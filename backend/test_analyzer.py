from app.services.analyzer import analyze_code

code = '''
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("zero")
    return a / b
'''

print(analyze_code(code))
