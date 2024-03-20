# Sushi Telegram Bot

Welcome to Sushi Telegram Bot, your ultimate destination for ordering delicious sushi dishes right from your Telegram app!

![image](https://github.com/romchhh/Sushi-Order-Telegram-Bot/assets/123520267/beebc917-9352-4aea-af07-4ed0f1fe7154)


## Features

### For Users:
- **Explore Menu:** Browse through a wide variety of sushi options, including rolls, sets, and maki.
- **Add to Cart:** Select your favorite items and add them to your cart with just a tap.
- **Place Orders:** Easily place orders by providing your contact details and confirming your selection.
- **Order Confirmation:** Receive a confirmation message with all the details of your order.

### For Admins:
- **Admin Panel:** Access an intuitive admin panel to manage the bot's settings and view analytics.
- **Statistics:** Monitor key metrics such as total users, active users, and sales to track the bot's performance.
- **Export Database:** Export the order database to Excel for further analysis and reporting.

## Usage

1. **Explore the Menu:** Start a conversation with the bot and use the command `/start` to begin.
2. **Add to Cart:** Browse the menu by selecting "Меню 📋" and add items to your cart.
3. **Place Orders:** Proceed to the cart using "Корзина 🛒" and follow the prompts to complete your order.
4. **Admin Features:** Admins can access the admin panel with the `/admin` command to manage the bot and view statistics.

## In use


https://github.com/romchhh/Sushi-Order-Telegram-Bot/assets/123520267/2f28bb7f-b0e9-4664-9b97-7623587c394c



## Requirements

- Python 3.6 or higher
- Libraries: aiogram

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your Telegram bot token, group ID, admin IDs, session name, API hash, API ID, and other configurations in the `config.py` file.

```python
TOKEN = 'your telegram bot token'
GROUP_ID = 'group id where the orders are sent forward'
ADMIN_IDS = [admin ids here]

```

5. Run the bot using `python main.py`.

## Contributing

Contributions are welcome! If you have any suggestions or find any bugs, feel free to open an issue or submit a pull request.

## License

[Include information about the license used for the project, e.g., MIT License]
