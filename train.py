import argparse
from detectors.bot_detection_trainer import BotDetectionTrainer

def main():
    parser = argparse.ArgumentParser(description='Bot Detection Trainer')
    a = 'store_true'
    help_ = 'Evaluate the bot detection model with cross-validation'
    parser.add_argument('--evaluate', action=a, default=False, help=help_)
    help_ = 'Save the bot detection model as TensorFlow.js model'
    parser.add_argument('--save', action=a, default=False, help=help_)

    args = parser.parse_args()

    trainer = BotDetectionTrainer()
    if args.evaluate:
        trainer.evaluate_bot_detection()
    if args.save:
        trainer.save_bot_detection_model()
    print("Done.")

if __name__ == '__main__':
    main()