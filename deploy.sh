
set -eu
ENV_NAME="${1:?Использование: deploy.sh <staging|production> [образ]}"
IMAGE="${2:-не указан}"
echo "Развёртывание образа ${IMAGE} в окружение ${ENV_NAME} (заглушка)"
