# 示例项目

项目结构：
```
my-project/
├── src/
│   ├── tasks/
│   │   ├── clean.py
│   │   ├── build.py
│   │   ├── watch.py
│   │   └── serve.py
│   ├── steps/
│   │   ├── clean_step.py
│   │   ├── sass_step.py
│   │   ├── uglify_step.py
│   │   ├── concat_step.py
│   │   ├── imagemin_step.py
│   │   └── browserSync_step.py
│   └── loaders/
│       ├── image_loader.py
│       ├── script_loader.py
│       ├── style_loader.py
│       └── ...
├── workflows/
│   ├── build.yaml
│   ├── deploy.yaml
│   └── ...
├── assets/
│   ├── images/
│   ├── styles/
│   └── scripts/
├── dist/
├── .env
├── .env.development
├── .env.production
└── workflow.py
```


- `src/` 目录存放开发者自定义的任务、步骤和加载器。
  - `tasks/` 目录存放具体的任务，文件名表示任务的功能，如 `clean.py`、`build.py` 等。
  - `steps/` 目录存放具体的步骤，文件名表示步骤的功能，如 `clean_step.py`、`sass_step.py` 等。
  - `loaders/` 目录存放自定义的加载器，用于加载不同类型的资源，如 `image_loader.py`、`script_loader.py` 等。
- `workflows/` 目录存放以 YAML 格式定义的工作流，如 `build.yaml`、`deploy.yaml` 等。
- `assets/` 目录存放项目的静态资源，如图片、样式表、脚本等。
- `dist/` 目录存放构建后的输出文件。
- `.env` 文件存放环境变量，可以根据不同环境（如开发、生产）设置不同的环境变量文件。
- `workflow.py` 文件是项目的入口文件，类似于 `gulpfile.js`，用于定义任务和工作流。

使用方式：

1. 在 `src/tasks/`、`src/steps/` 和 `src/loaders/` 目录中定义自定义的任务、步骤和加载器。

2. 在 `workflow.py` 文件中定义任务和工作流，例如：

```python
# workflow.py
from workflow import task, series, parallel, watch, src, dest, env
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
```

3. 在项目根目录下运行 Workflow 命令，例如：

```bash
workflow run --mode development
```

这将加载 `.env`、`.env.development` 和 `.env.development.local` 文件中的环境变量，并执行 `default` 任务。

以上只是一个简单的示例，实际项目中可以根据需要进行更复杂的配置和定义。

关于 Workflow 库本身的实现，我建议：

- `Task` 类表示一个任务，可以包含多个步骤（`Step`）或子任务，支持串行和并行执行。
- `Step` 类表示一个步骤，执行具体的操作，类似于 Gulp 中的 `pipe`。
- `Workflow` 类表示一个工作流，包含多个任务（`Task`），可以定义任务的执行顺序。
- `Config` 类表示配置，用于管理环境变量、任务配置、步骤配置、加载器配置等。
- `Loader` 类表示加载器，用于加载不同类型的资源，类似于 Webpack 中的 `Loader`。
- `Source` 类表示数据源，可以是文件、目录、URL 等，类似于 Gulp 中的 `src`。
- `Destination` 类表示输出目标，可以是文件、目录等，类似于 Gulp 中的 `dest`。

这样，开发者可以通过 Python 代码来定义任务和工作流，并通过 Workflow 命令来执行。同时，开发者也可以根据需要自定义任务、步骤、加载器等。

