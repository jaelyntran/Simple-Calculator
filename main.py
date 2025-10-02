from simple_calculator_ui import SimpleCalculator

calculation_history = []

if __name__ == '__main__':
    application = SimpleCalculator(history=calculation_history)
    application.mainloop()
