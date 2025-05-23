from celery import shared_task

from .utils import ModelTrainer


@shared_task
def train_ml_model_task(model_name):
    trainer = ModelTrainer(model_name)
    trainer.run()
