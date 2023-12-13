class nod_operation():
    def get_nod(num1, num2):
        while num1 != 0 and num2 != 0:
            if num1 >= num2:
                num1 -= num2
            else:
                num2 -= num1
        return num1 or num2