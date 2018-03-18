import traceback


while True:
    print("...")
    try:
        s = input(">")
        i = int(s)
        if i == 0:
            raise ValueError("i don't be zero")

        assert i > 0, f"{i} less by zero"

    except ValueError as err:
        print(f"error: {str(err)}: " + err.args[0])

    except KeyboardInterrupt as err:
        print("buy!" + traceback.print_exc())
        break

    except AssertionError as err:
        print("assert: " + err.args[0])
        break

    else:
        print(f"i = {i}")
    finally:
        print("finally")