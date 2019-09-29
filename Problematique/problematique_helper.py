
def add_if_far_enough(some_list, element_to_add, accept_factor):
    if element_to_add == None or element_to_add == 0.0:
        return some_list
    for element in some_list:
        element_l = element * (1.0 - accept_factor)
        element_h = element * (1.0 + accept_factor)
        if element_to_add >= element_l and element_to_add <= element_h:
            return some_list
    some_list.append(element_to_add)
    sorted(some_list)
    return some_list

