from data_handler.data_handler import DataHandler

def main():
    data_handler = DataHandler()
    data_handler.save_mev_bots_in_base_dataset(1000,10000)

if __name__ == '__main__':
    main()