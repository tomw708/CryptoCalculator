###
### HELPER FUNCTIONS FOR CRYPTOCALCULATOR APP
### MATHS EQUATIONS ETC
###

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False