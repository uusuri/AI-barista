import pandas as pd

path = "/Users/uusuri/Documents/PycharmProjects/Education/coffee_stock.xlsx"

try:
    df = pd.read_excel(path)
except FileNotFoundError:
    print("❌ Файл с остатками не найден!")
    exit()


def split_input(input_str):
    return [item.strip() for item in input_str.split(',') if item.strip()]


def validate_input(item, amount_str, mode="order"):
    try:
        amount = int(amount_str)
        if mode == "order" and amount <= 0:
            print(f"⚠️ Для '{item}': введите число больше 0!")
            return None
        elif mode == "restock" and amount < 0:
            print(f"⚠️ Для '{item}': количество не может быть отрицательным!")
            return None
    except ValueError:
        print(f"❌ Для '{item}': введите целое число!")
        return None
    return amount


def update_stock(item, amount, mode="order"):
    if item not in df["Название"].values:
        print(f"❌ Ошибка: '{item}' нет в списке!")
        return False, 0

    index = df.index[df["Название"] == item].tolist()[0]
    current_qty = df.at[index, "Количество"]

    if mode == "order":
        if current_qty < amount:
            print(f"⚠️ Для '{item}': недостаточно! Осталось: {current_qty}")
            return False, 0
        df.at[index, "Количество"] -= amount
        cost = df.at[index, "Стоимость"] * amount
        print(f"✅ Обновлено: {item} -{amount}. Остаток: {df.at[index, 'Количество']}")
        return True, cost
    else:  # restock
        df.at[index, "Количество"] = amount
        print(f"✅ Обновлено: {item} → {amount}")
        return True, 0


def restock_items():
    print("\n🔹 Режим пополнения остатков:")
    print(df)
    items = split_input(input("Введите названия позиций через запятую: "))
    amounts = split_input(input("Введите новые количества через запятую: "))

    if len(items) != len(amounts):
        print("❌ Ошибка: количество позиций не совпадает с количеством чисел!")
        return

    for item, amount_str in zip(items, amounts):
        amount = validate_input(item, amount_str, mode="restock")
        if amount is not None:
            update_stock(item, amount, mode="restock")

    df.to_excel(path, index=False)
    print("\nОбновленные остатки:")
    print(df)


def process_order():
    print("\n🔹 Текущие остатки:")
    print(df)

    user_input = input("\nВведите названия напитков через запятую или 'Пополнить': ").strip()

    if user_input.lower() == "пополнить":
        restock_items()
        return

    items = split_input(user_input)
    amounts = split_input(input("Введите количества через запятую: "))

    if len(items) != len(amounts):
        print("❌ Ошибка: количество напитков не совпадает с количеством чисел!")
        return

    total_cost = 0
    for item, amount_str in zip(items, amounts):
        amount = validate_input(item, amount_str, mode="order")
        if amount is not None:
            success, cost = update_stock(item, amount, mode="order")
            if success:
                total_cost += cost

    print(f"\nИтоговая стоимость: {total_cost}")
    df.to_excel(path, index=False)


def low_stock():
    low_items = {item: qty for item, qty in zip(df["Название"], df["Количество"]) if qty <= 3}
    return str(low_items) if low_items else "Нет позиций с низким остатком."


if __name__ == "__main__":
    process_order()
    print("\nОбновленные остатки:")
    print(df)