import pandas as pd

path = "/Users/uusuri/Documents/PycharmProjects/Education/coffee_stock.xlsx"

try:
    df = pd.read_excel(path)
except FileNotFoundError:
    print("No coffee stock found")
    exit()


def restock_items():
    print("\n🔹 Режим пополнения остатков:")
    print("Текущие остатки:")
    print(df)

    items_input = input("\nВведите названия позиций через запятую: ").strip()
    items = [item.strip() for item in items_input.split(',') if item.strip()]

    amounts_input = input("Введите новые количества через запятую: ").strip()
    amounts = [amount.strip() for amount in amounts_input.split(',') if amount.strip()]

    if len(items) != len(amounts):
        print("❌ Ошибка: количество позиций не совпадает с количеством чисел!")
        return

    for item, amount_str in zip(items, amounts):
        try:
            amount = int(amount_str)
            if amount < 0:
                print(f"⚠️ Для '{item}': количество не может быть отрицательным!")
                continue
        except ValueError:
            print(f"❌ Для '{item}': введите целое число!")
            continue

        if item not in df["Название"].values:
            print(f"❌ Ошибка: '{item}' нет в списке!")
            continue

        index_of_row = df.index[df["Название"] == item].tolist()[0]
        df.at[index_of_row, "Количество"] = amount
        print(f"✅ Обновлено: {item} → {amount}")

    df.to_excel(path, index=False)
    print("\nОбновленные остатки:")
    print(df)


def update_order():
    bill_summ = 0
    print("Текущие остатки:")
    print(df)

    user_input = input("\nВведите название напитка или 'Пополнить': ").strip()

    if user_input.lower() == "пополнить":
        restock_items()
        return

    items_input = user_input
    items = [item.strip() for item in items_input.split(',') if item.strip()]

    amounts_input = input("Введите количества через запятую: ").strip()
    amounts = [amount.strip() for amount in amounts_input.split(',') if amount.strip()]

    if len(items) != len(amounts):
        print("❌ Ошибка: количество позиций не совпадает с количеством чисел!")
        return

    for item, amount_str in zip(items, amounts):
        try:
            amount = int(amount_str)
            if amount <= 0:
                print(f"⚠️ Для '{item}': введите число больше 0!")
                continue
        except ValueError:
            print(f"❌ Для '{item}': введите целое число!")
            continue

        if item not in df["Название"].values:
            print(f"❌ Ошибка: '{item}' нет в списке!")
            continue

        index_of_row = df.index[df["Название"] == item].tolist()[0]

        if df.at[index_of_row, "Количество"] < amount:
            print(f"⚠️ Для '{item}': недостаточно! Осталось: {df.at[index_of_row, 'Количество']}")
            continue

        df.at[index_of_row, "Количество"] -= amount
        bill_summ += df.at[index_of_row, "Стоимость"] * amount
        print(f"✅ Обновлено: {item} -{amount}. Остаток: {df.at[index_of_row, 'Количество']}")

    print(f"\nИтоговая стоимость: {bill_summ}")
    df.to_excel(path, index=False)


def low_stock():
    res = {}
    for i in range(len(df["Название"].tolist())):
        if df["Количество"].tolist()[i] <= 3:
            res.update({df["Название"].tolist()[i]: df["Количество"].tolist()[i]})
    return str(res)


if __name__ == "__main__":
    update_order()
    print("\nИтоговые остатки:")
    print(df)