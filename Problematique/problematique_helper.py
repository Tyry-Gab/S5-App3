
def is_in_list_with_tolerance(some_list, element_to_add, accept_factor):
    if element_to_add == None or element_to_add == 0.0:
        return False
    for element in some_list:
        element_l = element[0] * (1.0 - accept_factor)
        element_h = element[0] * (1.0 + accept_factor)
        if element_to_add >= element_l and element_to_add <= element_h:
            return False
    return True

