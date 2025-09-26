from colorama import Fore, Style


def node_print(content: str, /):
    print(f"{Fore.GREEN}────┤ {content: ^50} ├────{Style.RESET_ALL}")


if __name__ == "__main__":
    node_print("This is a custom print message.")
