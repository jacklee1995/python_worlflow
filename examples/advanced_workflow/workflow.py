# workflow.py
from workflow_engine import task, series, parallel, watch, src, dest, env
from src.steps.clean_step import clean_step
from src.steps.sass_step import sass_step
from src.steps.uglify_step import uglify_step
from src.steps.concat_step import concat_step
from src.steps.imagemin_step import imagemin_step
from src.steps.browserSync_step import browserSync_step

@task
def clean():
    return src('dist/').pipe(clean_step())

@task
def styles():
    return src('assets/styles/**/*.scss') \
        .pipe(sass_step()) \
        .pipe(concat_step('styles.css')) \
        .pipe(dest('dist/css/')) \
        .pipe(browserSync_step.stream())

@task
def scripts():
    return src('assets/scripts/**/*.js') \
        .pipe(uglify_step()) \
        .pipe(concat_step('app.js')) \
        .pipe(dest('dist/js/')) \
        .pipe(browserSync_step.stream())

@task
def images():
    return src('assets/images/**/*') \
        .pipe(imagemin_step()) \
        .pipe(dest('dist/images/'))

@task
def serve():
    browserSync_step.init(server={'baseDir': './'})
    watch('assets/styles/**/*.scss', styles)
    watch('assets/scripts/**/*.js', scripts)
    watch('assets/images/**/*', images)
    watch('*.html').on('change', browserSync_step.reload)

@task
def build():
    return series(clean, parallel(styles, scripts, images))

@task
def default():
    return series(build, parallel(watch, serve))