import pyperclip

def print_numbers_from_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        max_number = int(clipboard_content.strip())
        if max_number < 1:
            print("Please copy a positive integer to the clipboard.")
            return

        numbers = list(range(1, max_number + 1))
        print(numbers)
    except ValueError:
        print("The content of the clipboard is not a valid integer. Please copy a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print_numbers_from_clipboard()