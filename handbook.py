"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine
if their course can be taken or not.

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
import re

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

def beautify_conditions(conditions):
    for course in conditions:
        conditions[course] = ' '.join(conditions[course].split())
        conditions[course] = conditions[course].lower()
        conditions[course] = conditions[course].replace('.', '')
        conditions[course] = conditions[course].replace(':', '')
        conditions[course] = conditions[course].replace(',', ' and')
        conditions[course] = conditions[course].replace('pre-requisite', '')
        conditions[course] = conditions[course].replace('pre-req', '')
        conditions[course] = conditions[course].replace('prequisite', '')
        conditions[course] = conditions[course].replace('prerequisite', '')
        conditions[course] = conditions[course].replace('completion of', '')
        conditions[course] = conditions[course].replace('4951', 'comp4951')
        conditions[course] = conditions[course].replace('4952', 'comp4952')
        conditions[course] = conditions[course].replace('comp1927 or ((comp1521 or dpst1092) and comp2521)', 'comp1927 or (comp2521 and (comp1521 or dpst1092))')

    return conditions

def gen_list(courses_list, condition):
    or_list = []
    course_list = []
    if condition == [] or len(condition) == 1:
        return tuple(condition)

    idx = 0
    while idx < len(condition):
        course = condition[idx]
        if course == 'or':
            if len(condition[idx-1]) == 8:
                or_list.append(condition[idx-1])
            if condition[idx+1] == condition[-1]:
                or_list.append(condition[-1])
        elif course == 'and':
            if len(condition[idx-1]) == 8:
                course_list.append(condition[idx-1])
                print(course_list)
            if condition[idx+1] == condition[-1]:
                course_list.append(condition[-1])
        elif course == '(':
            last_occur = len(condition) - 1 - condition[::-1].index(')')
            if condition[idx-1] != 'in':
                if condition[idx-1] == 'or':
                    or_list.append(gen_list(courses_list, condition[idx+1:last_occur+1]))
                else:
                    print(condition[idx+1:last_occur])
                    course_list.append(gen_list(courses_list, condition[idx+1:last_occur]))
            else:
                course_list.append(gen_list(courses_list, condition[0:condition.index(')')+1]))
            idx = last_occur
        elif course.isdigit() and condition[idx+1] == 'units':
            # the units of creadit should moved to the back of each string
            # print(condition[idx:len(condition)+1])
            course_list.append(check_credits(courses_list, condition[idx:len(condition)+1]))
            try:
                last_occur = len(condition) - 1 - condition[::-1].index(')')
                idx = last_occur
            except:
                idx = len(condition)

        idx += 1

    if or_list != []:
        if course_list != []:
            return or_list.append(course_list)
        else:
            return or_list
    else:
        return tuple(course_list)

def check_credits(courses_list, conditions):
    if conditions[0].isdigit():
        num_need = int(conditions[0])

    index = 1
    while index < len(conditions):
        course = conditions[index]
        if 'in' in conditions:
            if course == 'in':
                if conditions[index+1] == '(':
                    last_occur = len(conditions) - 1 - conditions[::-1].index(')')
                    generated = gen_list(courses_list, conditions[index+1:last_occur+1])
                    taken_num = 0
                    if isinstance(generated, tuple):
                        if isinstance(generated[0], tuple):
                            for course in generated[0]:
                                if course in courses_list:
                                    taken_num += 1
                        if isinstance(generated, str):
                            for course in generated:
                                if course in courses_list:
                                    taken_num += 1

                    print(taken_num)
                    print(num_need)
                    if taken_num*6 >= num_need:
                        return True
                    else:
                        return False
                    index = last_occur
                elif conditions[index+1] == 'level':
                    level_required = conditions[index+2]
                    all_require = conditions[index+3] + level_required
                    level_num = 0
                    for course in courses_list:
                        if all_require in course:
                            level_num += 1
                    if level_num*6 >= num_need:
                        return True
                    else:
                        return False
        else:
            if len(courses_list) * 6 >= num_need:
                result = True
            else:
                result = False

        index += 1
    return result

def check_valid(courses_list, gen_list):
    if courses_list == []:
        return False
    else:
        if isinstance(gen_list, tuple):
            return check_tuple(courses_list, gen_list)
        elif isinstance(gen_list, list):
            return check_list(courses_list, gen_list)

def check_list(courses_list, gen_list):
    result = False
    if isinstance(gen_list, tuple):
        result = check_tuple(courses_list, gen_list)
    for course in gen_list:
        if isinstance(course, str):
            if course in courses_list:
                result = True
        elif isinstance(course, tuple):
            if check_tuple(courses_list, course):
                result = True
    return result

# def check_list(courses_list, gen_list):
#     count = 0
#     count_str = 0
#     result = True
#     for course in gen_list:
#         if isinstance(course, str):
#             count_str += 1
#             if course not in courses_list:
#                 count += 1
#         elif isinstance(course, tuple):
#             result = result and check_tuple(courses_list, course)
#     if count == count_str:
#         result = result and False
#
#     return result

def check_tuple(courses_list, gen_list):
    result = True
    for course in gen_list:
        if course == False:
            return False
        if isinstance(course, str):
            if course not in courses_list:
                result = result and False
        elif isinstance(course, list):
            result = result and check_list(courses_list, course)
    return result

# def check_valid(courses_list, gen_list):
#     idx = 0
#     result = True
#     count_maybe_courses = 0
#     while idx < len(gen_list):
#         if gen_list[idx] == False:
#             result = result and False
#         elif gen_list[idx] == True:
#             result = result and True
#         elif isinstance(gen_list[idx], tuple):
#             for course in gen_list[idx]:
#                 if isinstance(course, list):
#                     result = result and check_valid(course)
#                 else:
#                     if course not in courses_list:
#                         result = result and False
#             result = result and check_valid(gen_list[idx])
#         else:
#             count_maybe_courses += 1
#             count = 0
#             if gen_list[idx] not in courses_list:
#                 count += 1
#         if count == count_maybe_courses:
#             result = result and False
#         idx += 1
#
#     return result

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course
    can be unlocked by them.

    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    # store the prerequisite in a list
    # case one: course_one or course_two, i will store in a list in a list

    # first simplify the structure to make it easier to deal with
    simplified = beautify_conditions(CONDITIONS)

    condition = simplified[target_course]
    condition = re.split('(\W)', condition)
    condition = list(filter(lambda a: a != ' ' and a != '', condition))


    for i in range(len(courses_list)):
        courses_list[i] = courses_list[i].lower()
    final_list = gen_list(courses_list, condition)

    print(final_list)
    if target_course != 'COMP1511':
        finial_return = check_valid(courses_list, final_list)
    else:
        finial_return = True
    print(finial_return)

    return finial_return

# is_unlocked([], ["COMP1511"])
# is_unlocked([], ["COMP1531"])
# is_unlocked([], ["COMP2511"])
# is_unlocked([], ["COMP2121"])
# is_unlocked([], ["COMP3151"])
# is_unlocked([], ["COMP3900"])
# is_unlocked([], ['COMP3901'])
# is_unlocked([], 'COMP9301')
# is_unlocked(["COMP1911", "MTRN2500"], "COMP2121")
# print(gen_list([], ['comp6443', 'and', 'comp6843', 'and', 'comp6445', 'and', 'comp6845', 'and', 'comp6447']))
# is_unlocked(["COMP1511", "COMP1521", "COMP1531", "COMP2521"], "COMP4161")
is_unlocked(["COMP9417", "COMP9418", "COMP9447"], "COMP9491")
