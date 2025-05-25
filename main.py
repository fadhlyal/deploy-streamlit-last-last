import streamlit as st
import os
import glob
from ast import literal_eval
import subprocess
import sys
import ctypes
import pandas as pd
import re

from openai import OpenAI

# Import clara components
from clara.interpreter import getlanginter
from clara.parser import getlangparser
from clara.feedback import Feedback, FeedGen
from clara.feedback_python import PythonFeedback

path = os.getenv("LD_LIBRARY_PATH", "")
build_path = os.getenv("build_path", "")
key = os.getenv("API_KEY", "")

if "/mount" in path and not (os.path.exists(build_path)) :
    subprocess.run([sys.executable, 'setup.py', 'build_ext', '--inplace'], check=True)

    lib_path = os.path.join(path, 'liblpsolve55.so')
    ctypes.CDLL(lib_path)

# Configure Streamlit page
st.set_page_config(
    page_title="Clara Feedback Analysis",
    page_icon="🔍",
    layout="wide"
)

def load_program(uploaded_file):
    """Helper function to load and parse program from uploaded file"""
    if uploaded_file is None:
        return None, None

    try:
        # Read content of uploaded file
        content = uploaded_file.getvalue().decode("utf-8")

        # Get file extension to determine language
        file_extension = uploaded_file.name.split('.')[-1]

        # Get parser for the language
        parser = getlangparser(file_extension)

        # Parse the code
        model = parser.parse_code(content)
        model.name = uploaded_file.name

        return model, file_extension
    except Exception as e:
        st.error(f"Error loading program: {str(e)}")
        return None, None

def load_correct_programs(cluster_dir, lang):
    """Load correct programs from clusters directory"""
    correct_programs = []
    try:
        for f in glob.glob(os.path.join(cluster_dir, f"*.{lang}")):
            with open(f, 'r', encoding='utf-8') as file:
                parser = getlangparser(lang)
                model = parser.parse_code(file.read())
                model.name = f
                correct_programs.append(model)
    except Exception as e:
        st.error(f"Error loading cluster programs: {str(e)}")
    return correct_programs

import logging

def load_adaptive_feedback(previous_code, difficulty, repair_suggestion):
    if previous_code and difficulty and repair_suggestion:
        adaptive_prompt = f"""
            You are an intelligent programming tutor that gives adaptive feedback to students based on the difficulty of the coding problem they attempted. Your tone and depth of explanation should vary depending on how difficult the problem is.

            Here is what you need to do:
            Given:
            1. The student's submitted code.
            2. The difficulty level of the problem ("easy", "medium", or "hard").
            3. The suggested repair/fix for their code.

            Your task is to:
            - Analyze the student's intent from the code.
            - Identify the issue based on the repair suggestion.
            - Generate feedback that is aligned with the difficulty:
            - For EASY problems:
                - Provide light, friendly feedback.
                - Focus on recalling simple concepts like arithmetic or basic syntax.
                - Provide a gentle hint instead of the full solution.
            - For MEDIUM problems:
                - Provide structured guidance.
                - Break down the logic and point to specific areas in their code.
                - Help them reason through the fix without just handing it over.
            - For HARD problems:
                - Encourage abstract reasoning and critical thinking.
                - Focus on their algorithmic approach.
                - Emphasize the "why" of the issue, not just the "how" to fix it.
            - Don't use the hint for the exactly right answer
            - Just give the output only don't mention extra information about language that be used, and difficulty level
            - Make more simple max 100-120 words
            - Use only one output and translate the output into Bahasa Indonesia
            - Don't show the original output that not be translated

            The input will be given like this:
            Previous code:
            {previous_code}

            Difficulty Problem:
            {difficulty}

            Repair suggestion:
            {repair_suggestion}

            Provide your output in this format:
            ---
            <your feedback here>
            ---
            """

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=key
            )

            completion = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=[
                    {
                        "role": "user",
                        "content": adaptive_prompt
                    }
                ]
            )

            return completion

        except Exception as e:
            logging.error("Error generating adaptive feedback: %s", e)
            return None

    return None

def rearrange_feedback(repair_suggestion):
    if repair_suggestion:
        prompt = f"""
            You are a code-aware translator. Your job is to rearrange the Input according to logical or execution order and then translate each line of the Input from English to Bahasa Indonesia.

            Here is what you need to do:
            Given:
            1. The suggested repair/fix for their code.

            Your task is to:
            1. Translate the input from English to Bahasa Indonesia
            2. Maintain code formatting where present.
            3. Do not translate keywords in Single quotes('') and Double quotes("")
            4. Output only the final translated and rearranged text or code like the Input

            Input:
            {repair_suggestion}
            """

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=key
            )

            completion = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return completion

        except Exception as e:
            logging.error("Error generating adaptive feedback: %s", e)
            return None

    return None

def main():
    try:
        st.title("Clara Feedback Analysis")

        # Side Bar
        st.sidebar.subheader("List Problem")
        problem_type = st.sidebar.radio(
            "Select Problem",
            ["problemA", "problemB", "problemC", "problemD", "problemE", "problemF"]
        )

        # Configuration
        verbose = False
        entry_func = problem_type
        timeout = 60

        # Program inputs
        args_input = ""
        ins_input = ""

        # Parse args and ins
        args = None
        ins = None

        if(problem_type == "problemA") :
            st.write("""
                ### Menghitung Luas Persegi
                Buatlah program dalam bahasa Python untuk menghitung luas persegi.

                ### Input Format
                Input dalam satu baris berupa sebuah bilangan bulat yang menyatakan sisi persegi.

                ### Output Format
                Output dalam satu baris berupa luas persegi dalam bilangan bulat.

                ### Constraints
                1 ≤ **sisi** ≤ 9999
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["2", "5", "15"],
                "Output": ["4", "25", "225"]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)

            st.markdown("""
                <style>
                .full-width-table {
                    width: 100%;
                    text-align: left;
                }

                .full-width-table th {
                    text-align: left;  /* Aligns the header text to the left */
                }
                </style>
            """, unsafe_allow_html=True)

            # Display the table without index and make it full width
            st.markdown(df.to_html(index=False, classes="full-width-table"), unsafe_allow_html=True)

            args_input = "[[[2]], [[5]], [[15]], [[43]], [[99]]]"
            type = "A"
            difficulty = "easy"
        elif(problem_type == "problemB") :
            st.write("""
                ### Bilangan Konsekutif Menaik
                Buatlah program dalam bahasa Python untuk menentukan apakah bilangan-bilangan yang dimasukkan tersusun konsekutif menaik atau tidak. Contoh bilangan konsekutif menaik **2 3 4** atau **-3 -2 -1**.

                ### Input Format
                Input dalam satu baris berupa tiga bilangan bulat **a**, **b**, **c**.

                ### Output Format
                Output dalam satu baris berupa string **ya** jika konsekutif menaik, atau **tidak** jika tidak konsekutif menaik.

                ### Constraints
                -9999 ≤ **a**, **b**, **c** ≤ 9999
            """)
            st.write("### Samples")
            data = {
                "Input": ["1 2 3", "2 2 1", "3 4 -5"],
                "Output": ["ya", "tidak", "tidak"]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)

            st.markdown("""
                <style>
                .full-width-table {
                    width: 100%;
                    text-align: left;
                }

                .full-width-table th {
                    text-align: left;  /* Aligns the header text to the left */
                }
                </style>
            """, unsafe_allow_html=True)

            # Display the table without index and make it full width
            st.markdown(df.to_html(index=False, classes="full-width-table"), unsafe_allow_html=True)

            args_input = "[[[1, 2, 3]], [[2, 2, 1]], [[4, 3, 4]], [[3, 4, 3]], [[3, 4, -5]]]"
            type = "B"
            difficulty = "easy"
        elif(problem_type == "problemC") :
            st.write("""
                ### Dadu Genap
                Tiga buah dadu (d1, d2, d3) bermata enam dilemparkan. Buatlah program dalam bahasa Python untuk memeriksa apakah mata dadu yang muncul semuanya genap atau tidak.

                ### Input Format
                Input dalam satu baris berupa Tiga buah bilangan bulat yang menyatakan mata dadu **d1**, **d2**, dan **d3**.

                ### Output Format
                Output dalam satu baris berupa Boolean **True** jika ketiga mata dadu yang muncul semuanya genap atau **False** jika tidak.

                ### Constraints
                1 ≤ **d1**, **d2**, **d3** ≤ 6
            """)
            st.write("### Samples")
            data = {
                "Input": ["3 3 3", "2 4 6", "1 2 3"],
                "Output": ["False", "True", "False"]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)

            st.markdown("""
                <style>
                .full-width-table {
                    width: 100%;
                    text-align: left;
                }

                .full-width-table th {
                    text-align: left;  /* Aligns the header text to the left */
                }
                </style>
            """, unsafe_allow_html=True)

            # Display the table without index and make it full width
            st.markdown(df.to_html(index=False, classes="full-width-table"), unsafe_allow_html=True)

            args_input = "[[[3, 3, 3]], [[2, 4, 6]], [[1, 2, 3]], [[2, 2, 5]], [[4, 4, 6]]]"
            type = "C"
            difficulty = "medium"
        elif(problem_type == "problemD") :
            st.write("""
                ### Digit Genap dan Ganjil
                Buatlah program dalam bahasa Python untuk mencetak bilangan 1 atau 0.
                
                Cetak bilangan 1, jika digit awal bilangan yang diinput merupakan bilangan ganjil dan digit akhirnya merupakan bilangan genap. Selain dari itu cetak bilangan 0.

                ### Input Format
                Input dalam satu baris berupa satu buah bilangan bulat yang memiliki 4 digit, yaitu bilangan 1000 hingga 9999.

                ### Output Format
                Output dalam satu baris berupa sebuah bilangan **1** atau **0** bergantung dari nilai kondisinya..

                ### Constraints
                1000 ≤ **bilangan** ≤ 9999
            """)
            st.write("### Samples")
            data = {
                "Input": ["1000", "1001", "9999"],
                "Output": ["1", "0", "0"]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)

            st.markdown("""
                <style>
                .full-width-table {
                    width: 100%;
                    text-align: left;
                }

                .full-width-table th {
                    text-align: left;  /* Aligns the header text to the left */
                }
                </style>
            """, unsafe_allow_html=True)

            # Display the table without index and make it full width
            st.markdown(df.to_html(index=False, classes="full-width-table"), unsafe_allow_html=True)

            args_input = "[[[1000]], [[1001]], [[9999]], [[1234]], [[2332]]]"
            type = "D"
            difficulty = "medium"
        elif(problem_type == "problemE") :
            st.write("""
                ### Fall Guys Three
                Pada game Fall Guys Three terdapat sebuah program yang digunakan untuk menentukan apakah permainan berlanjut atau tidak (game over). Permainan berlanjut, jika

                - Nilai health pemain tidak bernilai 0, dan
                - Pemain berada pada level 1 dengan skor minimal 1000, atau
                - Pemain berada pada level 2 dengan skor minimal 3000, atau
                - Pemain berhasil mencapai skor 7000 untuk level berapapun.

                ### Input Format
                Input dalam satu baris berupa tiga buah bilangan bulat yang masing-masing menyatakan **health**, **score**, dan **level**.

                ### Output Format
                Output dalam satu baris berupa nilai boolean **True** apabila permainan selesai/gameover, dan **False** apabila pemain masih bisa melanjutkan permainan.

                ### Constraints
                - 0 ≤ **health** ≤ 999
                - 0 ≤ **score** ≤ 9999
                - 1 ≤ **level** ≤ 99
            """)
            st.write("### Samples")
            data = {
                "Input": ["1 1000 1", "0 1000 1", "21 6999 38"],
                "Output": ["False", "True", "True"]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)

            st.markdown("""
                <style>
                .full-width-table {
                    width: 100%;
                    text-align: left;
                }

                .full-width-table th {
                    text-align: left;  /* Aligns the header text to the left */
                }
                </style>
            """, unsafe_allow_html=True)

            # Display the table without index and make it full width
            st.markdown(df.to_html(index=False, classes="full-width-table"), unsafe_allow_html=True)

            args_input = "[[[1, 1000, 1]], [[0, 1000, 1]], [[1, 6999, 3]], [[0, 8993, 5]], [[1, 1622, 2]]]"
            type = "E"
            difficulty = "hard"
        elif(problem_type == "problemF") :
            st.write("""
                ### Menghitung Faktor Bilangan
                Buatlah program dalam bahasa Python untuk menghitung faktor dari suatu bilangan. Faktor adalah bilangan yang habis membagi suatu bilangan. Contoh:

                - Jumlah Faktor dari **15** adalah **4**, yaitu 1, 3, 5 dan 15.
                - Jumlah Faktor dari **24** adalah **8**, yaitu 1, 2, 3, 4, 6, 8, 12, dan 24.

                ### Input Format
                Input dalam satu baris berupa sebuah bilangan bulat positif **N**.

                ### Output Format
                Output dalam satu baris berupa sebuah bilangan yang menyatakan jumlah faktor dari suatu bilangan.

                ### Constraints
                1 ≤ **N** ≤ 9999
            """)
            st.write("### Samples")
            data = {
                "Input": ["15", "24"],
                "Output": ["4", "8"]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)

            st.markdown("""
                <style>
                .full-width-table {
                    width: 100%;
                    text-align: left;
                }

                .full-width-table th {
                    text-align: left;  /* Aligns the header text to the left */
                }
                </style>
            """, unsafe_allow_html=True)

            # Display the table without index and make it full width
            st.markdown(df.to_html(index=False, classes="full-width-table"), unsafe_allow_html=True)

            args_input = "[[[15]], [[24]], [[64]], [[23]], [[76]]]"
            type = "F"
            difficulty = "hard"
        try:
            if args_input.strip():
                args = literal_eval(args_input)
            if ins_input.strip():
                ins = literal_eval(ins_input)
        except Exception as e:
            st.error(f"Error parsing arguments or inputs: {str(e)}")
            return

        st.header("Generate Feedback for '" + problem_type + "'")

        # Upload incorrect program
        incorrect_program = st.file_uploader("Upload program for feedback", key="prog")
        if incorrect_program:
            kodingan = incorrect_program.getvalue().decode("utf-8")
            st.code(kodingan, language="python")

        # Cluster directory input
        cluster_dir = os.path.join(os.path.dirname(__file__), 'clusters/set2')
        cluster_dir = os.path.join(cluster_dir, type)

        max_cost = 0 #0 means no limit
        clean_strings = False #Clean Strings
        ignore_io = True #Input Output
        ignore_ret = False #Return Value

        #Use session state for max 3 attempt
        if 'type' not in st.session_state:
            st.session_state.type = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}

        is_disabled = st.session_state.type[type] >= 5

        if st.button("Generate Feedback", type="primary", disabled=is_disabled):
            if not incorrect_program:
                st.error("Please upload a program for feedback.")
                return

            model, lang = load_program(incorrect_program)
            if not model:
                return

            # Load correct programs from cluster
            correct_programs = load_correct_programs(cluster_dir, lang)
            if not correct_programs:
                st.error(f"No correct programs found in {cluster_dir}")
                return

            interpreter = getlanginter(lang)

            # Set feedback module
            feedmod = PythonFeedback

            feedgen = FeedGen(
                verbose=verbose,
                timeout=timeout,
                allowsuboptimal=True,
                feedmod=feedmod
            )

            with st.spinner("Generating feedback..."):
                try:
                    feedback = feedgen.generate(
                        model, correct_programs, interpreter,
                        ins=ins, args=args,
                        ignoreio=ignore_io,
                        ignoreret=ignore_ret,
                        cleanstrings=clean_strings,
                        entryfnc=entry_func
                    )

                    if feedback.status == Feedback.STATUS_REPAIRED:
                        if max_cost > 0 and feedback.cost > max_cost:
                            st.error(f'Max cost exceeded ({feedback.cost} > {max_cost})')
                        else:
                            if(st.session_state.type[type] >= 4) :
                                st.session_state.type[type] += 1
                                if feedback.feedback :
                                    st.error("Answer is Incorrect")
                                else :
                                    st.success("Answer is Correct")
                            elif feedback.feedback :
                                st.session_state.type[type] += 1

                                # Make the feedback more readable
                                cleaned_feedback = [re.sub(r"\s*\(cost=\d+(\.\d+)?\)", "", s) for s in feedback.feedback]
                                cleaned_feedback = [s.replace("assignment", "variable") for s in cleaned_feedback]
                                cleaned_feedback = [s.replace("statement", "variable") for s in cleaned_feedback]
                                cleaned_feedback = [re.sub(r"\$(\w+)", r"\1", s) for s in cleaned_feedback]
                                cleaned_feedback = [re.sub(r"\bat (\d+)\b", r"at line \1", s) for s in cleaned_feedback]

                                if(st.session_state.type[type] == 4) :
                                    adaptive_feedback = rearrange_feedback(cleaned_feedback)
                                else :
                                    adaptive_feedback = load_adaptive_feedback(kodingan, difficulty, cleaned_feedback)

                                st.success("Feedback generated successfully!")
                                st.subheader("Feedback:")

                                st.text_area("", value=adaptive_feedback.choices[0].message.content, height=300, disabled=True)
                            else :
                                st.success("Answer is Correct")
                    elif feedback.status == Feedback.STATUS_ERROR:
                        st.error(f"Error generating feedback: {feedback.error}")
                    else:
                        st.warning(feedback.statusstr())

                except Exception as e:
                    st.error(f"Error generating feedback: {str(e)}")
                    if verbose:
                        st.exception(e)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        if verbose:
            st.exception(e)

if __name__ == "__main__":
    main()