
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from collections import defaultdict
from apis.models import (SchoolStructure, Schools, Classes, Personnel,
                         Subjects, StudentSubjectsScore)


class StudentSubjectsScoreAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.
                    - Credit must be integer, greater than 0 and equal or less than 3.
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - If Update, Credit must not be changed.
                    - If Data Payload not complete return clearly message with bad request status.
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    - If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]

        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subject_title", None)
        score = request.data.get("score", None)

        if None in [student_first_name, student_last_name, subjects_title,
                    score]:
            return Response({"error": "Payload data is incomplete"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(student_first_name, str) or not isinstance(
                student_last_name, str) \
                or not isinstance(subjects_title, str):
            return Response(data={"error": "Invalid data type for string "
                                           "fields"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            score = float(score)
            if not (0 <= score <= 100):
                return Response(data={"error": "Score must be between 0 and "
                                               "100"},
                                status=status.HTTP_400_BAD_REQUEST)
            student = Personnel.objects.get(first_name=student_first_name,
                                            last_name=student_last_name)
            subject = Subjects.objects.get(title=subjects_title)
            credit_id = None
            credit = None
            for mapping in credits_mapping:
                if mapping['subject_id'] == subject.id:
                    credit_id = mapping["credit_id"]
                    break
            for mapping in credits_context:
                if mapping['id'] == credit_id:
                    credit = mapping['credit']

        except ValueError as e:
            return Response(data={"error": "Invalid data type for score, "
                                           "must be a number"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Personnel.DoesNotExist:
            return Response({"error": "Student not found"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Subjects.DoesNotExist:
            return Response({"error": "Subject not found"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            score_entry = StudentSubjectsScore.objects.get(student=student,
                                                           subjects=subject)
            score_entry.score = score
            score_entry.save()
        except StudentSubjectsScore.DoesNotExist:
            StudentSubjectsScore.objects.create(student=student,
                                                subjects=subject,
                                                credit=credit,
                                                score=score)

        # # Filter Objects Example
        # DataModel.objects.filter(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        # # Create Objects Example
        # DataModel.objects.create(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        response_data = {
            "student_first_name": student_first_name,
            "student_last_name": student_last_name,
            "subject_title": subjects_title,
            "credit": credit,
            "score": score
        }

        return Response(data=response_data, status=status.HTTP_201_CREATED)


def calculate_grade(score):
    if 80 <= score <= 100:
        return "A"
    elif 75 <= score < 80:
        return "B+"
    elif 70 <= score < 75:
        return "B"
    elif 65 <= score < 70:
        return "C+"
    elif 60 <= score < 65:
        return "C"
    elif 55 <= score < 60:
        return "D+"
    elif 50 <= score < 55:
        return "D"
    else:
        return "F"


class StudentSubjectsScoreDetailsAPIView(APIView):



    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """

        student_id = kwargs.get("id", None)

        try:
            student = Personnel.objects.get(
                id=student_id)

            student_subjects_scores = StudentSubjectsScore.objects.filter(
                student=student)

        except Personnel.DoesNotExist:
            return Response({"error": "Student not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except StudentSubjectsScore.DoesNotExist:
            return Response({"error": "Score not found"},
                            status=status.HTTP_404_NOT_FOUND)

        subject_details = []

        for student_subjects_score in student_subjects_scores:

            if student_subjects_score:
                score = student_subjects_score.score
                credit = student_subjects_score.credit
                grade = calculate_grade(score)
                subject = student_subjects_score.subjects
                subject_detail = {
                    "subject": subject.title,
                    "credit": credit,
                    "score": score,
                    "grade": grade,
                }
                subject_details.append(subject_detail)

        total_score = sum(
            detail['score'] * detail['credit'] for detail in subject_details)
        total_credits = sum(detail['credit'] for detail in subject_details)
        if total_credits != 0:
            gpa = total_score / total_credits
        else:
            gpa = 0

        fullname = student.first_name + " " + student.last_name
        school = student.school_class.school.title

        student_data = {
            "id": student.id,
            "full_name": fullname,
            "school": school,
        }

        response_data = {
            "student": student_data,
            "subject_details": subject_details,
            "grade_point_average": f'{format(gpa, ".2f")}',
        }

        example_context_data = {
            "student":
                {
                    "id": "primary key of student in database",
                    "full_name": "student's full name",
                    "school": "student's school name"
                },

            "subject_detail": [
                {
                    "subject": "subject's title 1",
                    "credit": "subject's credit 1",
                    "score": "subject's score 1",
                    "grade": "subject's grade 1",
                },
                {
                    "subject": "subject's title 2",
                    "credit": "subject's credit 2",
                    "score": "subject's score 2",
                    "grade": "subject's grade 2",
                },
            ],

            "grade_point_average": "grade point average",
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PersonnelDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """


        school_title = kwargs.get("school_title", None)

        try:
            school = Schools.objects.get(title=school_title)
            classes = Classes.objects.filter(school=school)
            result = Personnel.objects.filter(
                school_class__school__title=school_title
            ).annotate(
                school_title=F('school_class__school__title'),
                class_order=F('school_class__class_order')
            ).values(
                'school_title', 'class_order', 'first_name', 'last_name',
                'personnel_type'
            ).order_by(
                'personnel_type'
            )
            print(result)

            formatted_data = [
                f"{index + 1}. school: {item['school_title']}, role: {['Teacher', 'Head of the room', 'Student'][item['personnel_type']]}, class: {item['class_order']}, name: {item['first_name']} {item['last_name']}"
                for index, item in enumerate(result)
            ]

            for item in formatted_data:
                print(item)

        except Schools.DoesNotExist:
            return Response({"error": "School not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except Classes.DoesNotExist:
            return Response({"error": "Classes not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except Personnel.DoesNotExist:
            return Response({"error": "Personnel not found"},
                            status=status.HTTP_404_NOT_FOUND)

        your_result = [
            (f"{index + 1}. school: {item['school_title']}, "
             f"role:{['Teacher', 'Head of the room', 'Student'][item['personnel_type']]}, "
             f"class: {item['class_order']}, "
             f"name: {item['first_name']} {item['last_name']}")
            for index, item in enumerate(result)]

        return Response(your_result, status=status.HTTP_400_BAD_REQUEST)


class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        your_result = []
        teacher = None

        schools = Schools.objects.all()
        for school in schools:
            result = {
                "school": school.title
            }
            class_list = Classes.objects.filter(school=school).all()
            for classes in class_list:
                if classes.class_order not in result.keys():
                    result[f"class {classes.class_order}"] = {}
                personnels = Personnel.objects.filter(school_class=classes).all()
                for personnel in personnels:
                    full_name = f'{personnel.first_name} {personnel.last_name}'
                    if personnel.personnel_type == 0:
                        if "Teacher" not in result[f"class {classes.class_order}"].keys():
                            teacher = full_name
                            result[f"class {classes.class_order}"][f"Teacher: {teacher}"] = []
                    elif personnel.personnel_type == 1:
                        result[f"class {classes.class_order}"][f"Teacher: {teacher}"].append(
                            {"Head of the room": full_name}
                        )
                    else:
                        result[f"class {classes.class_order}"][f"Teacher: {teacher}"].append(
                            {"Student": full_name}
                        )
            your_result.append(result)

        return Response(your_result, status=status.HTTP_200_OK)


class SchoolStructureAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """

        def get_children(parent_node):
            children = []
            child_nodes = SchoolStructure.objects.filter(parent=parent_node)
            for child_node in child_nodes:
                child = {
                    'title': child_node.title,
                }
                grandchildren = get_children(child_node)
                if grandchildren:
                    child['sub'] = grandchildren
                children.append(child)
            return children

        your_result = []

        root_nodes = SchoolStructure.objects.filter(parent=None)
        for root_node in root_nodes:
            root = {
                'title': root_node.title,
                'sub': get_children(root_node)
            }
            your_result.append(root)

        return Response(your_result, status=status.HTTP_200_OK)
