from unittest.mock import MagicMock
from core.infrastructure.services import OrderService, OrderItem

def test_large_order():
    stock_repo = MagicMock()
    menu_repo = MagicMock()
    order_repo = MagicMock()

    menu_repo.get_recipe.side_effect = lambda name: {
        'раф лавандовый': {
            'ingredient': {'зерно арабика': 18.5, 'молоко лавандовое': 100, 'сливки': 50},
            'syrup': {'лавандовый': 15}
        },
        'американо': {
            'ingredient': {'зерно арабика': 18.5},
            'syrup': {}
        },
        'бамбл': {
            'ingredient': {'зерно арабика': 18.5, 'мед': 15, 'лимонный сок': 10},
            'syrup': {'ванильный': 10}
        },
        'латте': {
            'ingredient': {'зерно арабика': 18.5, 'молоко': 200},
            'syrup': {'лавандовый': 100}
        },
        'эспрессо тоник':{
            'ingredient': {'зерно арабика': 18.5, 'тоник': 150},
        }
    }[name]

    menu_repo.get_price.side_effect = lambda name: {
        'раф лавандовый': 360,
        'американо': 200,
        'бамбл': 350,
        'латте': 290,
        'эспрессо тоник': 250,
        'лавандовый': 40,
        'мятный': 40,
        'ванильный': 40
    }[name]

    stock_repo.has_items.return_value = True
    order_repo.create_order.return_value = 1

    service = OrderService(stock_repo, menu_repo, order_repo)

    order_items = [
        OrderItem(menu_item_name='раф лавандовый', quantity=1, syrup_name='мятный', syrup_quantity=10),
        OrderItem(menu_item_name='эспрессо тоник', quantity=1),
        OrderItem(menu_item_name='американо', quantity=1),
        OrderItem(menu_item_name='бамбл', quantity=1, syrup_name='ванильный', syrup_quantity=10),
        OrderItem(menu_item_name='латте', quantity=1, syrup_name='лавандовый', syrup_quantity=100)
    ]

    result = service.create_order("Test Customer", order_items, "cash")

    assert result['status'] == 'success'
    assert result['order_id'] == 1
    assert stock_repo.consume_items.called

    expected_ingredients = {
        'зерно арабика': 18.5 * 5,
        'молоко лавандовое': 100,
        'тоник': 150,
        'сливки': 50,
        'мед': 15,
        'лимонный сок': 10,
        'молоко': 200
    }

    actual_syrup_call = next(call_args[0][0] for call_args in stock_repo.consume_items.call_args_list
                             if call_args[0][1] == 'syrup')

    expected_syrups = {
        'лавандовый': 215,
        'мятный': 10,
        'ванильный': 20
    }

    assert actual_syrup_call == expected_syrups

    actual_calls = stock_repo.consume_items.call_args_list
    found_ingredients = any(call_args[0][0] == expected_ingredients and call_args[0][1] == 'ingredient'
                            for call_args in actual_calls)
    assert found_ingredients, f"Ingredients call not found. Actual calls: {actual_calls}"

    found_syrups = any(call_args[0][0] == expected_syrups and call_args[0][1] == 'syrup'
                       for call_args in actual_calls)
    assert found_syrups, f"Syrups call not found. Actual calls: {actual_calls}"
