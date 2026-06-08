import sys


# DATA NOT FOUND IN DB

def handle_empty_df(df, message):
    if df.empty:
        print(message)

    return df


# GET DATA FUNCTIONS -- INVALID INPUT

def validate_patient_id(patient_id):
    try:
        patient_id = str(patient_id)

        if len(patient_id) != 4:
            raise ValueError("ID must contain exactly 4 digits")

        for digit in patient_id:
            if not digit.isnumeric():
                raise TypeError("invalid - only numbers are allowed")

    except TypeError as err:
        print(sys.exc_info()[0], err)
        raise

    except ValueError as err:
        print(sys.exc_info()[0], err)
        raise

    finally:
        print("validation finished")



# INSERT FUNCTIONS --  INVALID INPUT

# INSERT PATIENT FUNCTION
def validate_patient_input(patient_id, full_name=None, date_of_birth=None,
                           gender=None, phone=None, email=None):
    try:
        patient_id = str(patient_id)

        if len(patient_id) != 4:
            raise ValueError("ID must contain exactly 4 digits")

        for digit in patient_id:
            if not digit.isnumeric():
                raise TypeError("invalid - only numbers are allowed")

        if full_name is not None and len(full_name) > 100:
            raise ValueError("Please enter valid full name")

        if gender is not None and gender not in ["Female", "Male", "Other"]:
            raise ValueError("Invalid gender value")

        if phone is not None:
            phone = str(phone)

            for digit in phone:
                if not digit.isnumeric():
                    raise TypeError("invalid - only numbers are allowed")

            if len(phone) > 20:
                raise ValueError("phone must contain up to 20 digits")

        if email is not None:
            if "@" not in email or "." not in email:
                raise ValueError("invalid email address")

            if len(email) > 100:
                raise ValueError("invalid email address")

    except TypeError as err:
        print(sys.exc_info()[0], err)
        raise

    except ValueError as err:
        print(sys.exc_info()[0], err)
        raise

    except BaseException as err:
        print(sys.exc_info()[0], err)
        raise

    finally:
        print("validation finished")


# INSERT ANALYSIS RESULT
def validate_analysis_result_input(session_id, modality, image_name, DME, DR,
                                   confidence_score=None):
    try:
        if not isinstance(session_id, int):
            raise TypeError("Session ID must be an integer")

        if modality not in ["Fundus", "OCT"]:
            raise ValueError("Modality must be Fundus or OCT")

        if image_name is None or image_name == "":
            raise ValueError("missing image name")

        if DME not in [0, 1]:
            raise ValueError("DME must be 0 or 1")

        if DR is not None and DR not in ["0", "NPDR", "PDR"]:
            raise ValueError("DR valid values are [0, NPDR, PDR, None]")
        

        if confidence_score is not None:
            if confidence_score < 0 or confidence_score > 1:
                raise ValueError("confidence score is out of range")

    except TypeError as err:
        print(sys.exc_info()[0], err)
        raise

    except ValueError as err:
        print(sys.exc_info()[0], err)
        raise

    finally:
        print("validation finished")