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
    # this functions is about to simplified the version of data and make them into format so that it is easier to deal with
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
            # the units of credit should moved to the back of each string
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
    print(conditions)
    print('first_conditions')
    # the first value of conditions should be a number
    if conditions[0].isdigit():
        num_need = int(conditions[0])

    index = 1
    while index < len(conditions):
        course = conditions[index]
        # in means we should check more about the courses, e.g. check if the course is comp level 3
        if 'in' in conditions:
            if course == 'in':
                # this situation is credit in (comp9417 and comp9418 and comp9444 and comp9447)
                # and we just deal with this as common brackets
                if conditions[index+1] == '(':
                    print(conditions[::-1])
                    print('conditions')
                    last_occur = len(conditions) - 1 - conditions[::-1].index(')')
                    generated = gen_list(courses_list, conditions[index+1:last_occur+1])
                    taken_num = 0
                    # this is a bit tricky, currently sometimes i have ((),) and sometimes i have ()
                    if isinstance(generated, tuple):
                        if isinstance(generated[0], tuple):
                            for course in generated[0]:
                                if course in courses_list:
                                    taken_num += 1
                        if isinstance(generated, str):
                            for course in generated:
                                if course in courses_list:
                                    taken_num += 1

                    # i check if the units of credit meet the creteria
                    if taken_num*6 >= num_need:
                        return True
                    else:
                        return False
                    index = last_occur
                elif conditions[index+1] == 'level':
                    # this situation is when credit in level 2 comp courses
                    # so we just check how many courses in the courses_list meet the creteria
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
            # no in in the list, that is only completion of units of credit needed
            # we just count the units of credit
            if len(courses_list) * 6 >= num_need:
                result = True
            else:
                result = False

        index += 1
    return result

def check_valid(courses_list, gen_list):
    # if the student has not taken any course before he cannot learn any course except COMP1511
    if courses_list == []:
        return False
    else:
        # if the result we received is tuple then we call check_tuple
        # if we received list then call check_list
        if isinstance(gen_list, tuple):
            return check_tuple(courses_list, gen_list)
        elif isinstance(gen_list, list):
            return check_list(courses_list, gen_list)

def check_list(courses_list, gen_list):
    result = False
    if isinstance(gen_list, tuple):
        result = check_tuple(courses_list, gen_list)
    # if any of the course in list has been taken before then return True
    for course in gen_list:
        if isinstance(course, str):
            if course in courses_list:
                result = True
        elif isinstance(course, tuple):
            if check_tuple(courses_list, course):
                result = True
    return result

def check_tuple(courses_list, gen_list):
    result = True
    # if any of the course in the tuple has not been taken before then return False
    for course in gen_list:
        if course == False:
            return False
        if isinstance(course, str):
            if course not in courses_list:
                result = result and False
        elif isinstance(course, list):
            result = result and check_list(courses_list, course)
    return result

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course
    can be unlocked by them.

    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    # store the prerequisite in a list
    # case one: course_one or course_two, i will store in a list in a list

    print(target_course)
    print('target')
    # first simplify the structure to make it easier to deal with
    simplified = beautify_conditions(CONDITIONS)

    condition = simplified[target_course]
    condition = re.split('(\W)', condition)
    condition = list(filter(lambda a: a != ' ' and a != '', condition))

    # first make very course in the courses_list in lower case, this is easier for later process
    for i in range(len(courses_list)):
        courses_list[i] = courses_list[i].lower()

    # get the final generated list
    # in this list, elements are not forced as long as one of them are taken
    # while elements in tuple have to be taken before, they are forced
    # list represents course_one or course_two
    # tuple represents course_one and course_two

    # comp9302 is a bit tricky in my solution so i decided to solve it separately
    if target_course == 'COMP9302':
        final_list = (['comp6441', 'comp6841'], check_credits(courses_list, ['12', 'in', '(', 'comp6443', 'and', 'comp6843', 'and', 'comp6445', 'and', 'comp6845', 'and', 'comp6447', ')']))
    else:
        final_list = gen_list(courses_list, condition)

    # COMP1511 is a bit different, if we are given with an empty list, only COMP1511 is true
    # so i decided to deal with this specifically

    if target_course == 'COMP1511':
        finial_return = True
    else:
        finial_return = check_valid(courses_list, final_list)

    return finial_return

is_unlocked(["COMP9417", "COMP9418", "COMP9447"], "COMP9491")
