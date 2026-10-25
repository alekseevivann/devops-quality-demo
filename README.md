# devops-quality-demo

Учебный проект к курсовой работе «Исследование методов обеспечения качества
в DevOps-практиках (Jenkins, GitLab CI, GitHub Actions)».

Небольшой веб-сервис на Flask (задачи, проверка сложения, `/health`) и
**один и тот же конвейер контроля качества, описанный для трёх систем CI/CD**:

| Система | Файл конфигурации | Приложение курсовой |
|---|---|---|
| Jenkins | `Jenkinsfile` | А |
| GitLab CI/CD | `.gitlab-ci.yml` | Б |
| GitHub Actions | `.github/workflows/ci.yml` | В |

Этапы конвейера: линтер (flake8) → модульные тесты и порог покрытия 80 %
(pytest, pytest-cov) → статический анализ безопасности (Bandit; CodeQL в GitHub,
шаблоны SAST и Secret Detection в GitLab) → сборка образа → staging →
ручное подтверждение → production. Скрипт `deploy.sh` — учебная заглушка.

## Локальный запуск проверок

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
flake8 app tests
pytest --cov=app --cov-fail-under=80
bandit -r app -ll
docker build -t demo-app . && docker run --rm -p 8000:8000 demo-app
```

## Как запустить конвейер

**GitHub Actions** (проще всего): создайте репозиторий на GitHub, отправьте
файлы (`git init`, `git add .`, `git commit`, `git push`) — вкладка *Actions*
покажет запуск. Для ручного подтверждения создайте окружения `staging` и
`production` (Settings → Environments) и в `production` включите *Required
reviewers*. В публичном репозитории это доступно бесплатно, в приватном —
зависит от тарифа; то же касается CodeQL.

**GitLab CI/CD**: импортируйте/отправьте проект на GitLab.com. Сборка образа
использует Docker-in-Docker и требует исполнителя с включённым privileged-режимом;
если такого нет, уберите задание `build_image`. Выкладка в production — кнопка
запуска вручную (`when: manual`).

**Jenkins**: `docker run -p 8080:8080 jenkins/jenkins:lts-jdk21`, установите
рекомендуемые плагины, создайте Multibranch Pipeline на этот репозиторий.
Агенту нужны Python 3, venv и Docker. Адрес реестра `registry.example.com`
в `Jenkinsfile` замените на свой или временно уберите этап сборки образа.

Что снять для приложения курсовой: успешный запуск конвейера, отчёт о тестах,
экран с ручным подтверждением выкладки и (в GitLab/GitHub) раздел безопасности.
