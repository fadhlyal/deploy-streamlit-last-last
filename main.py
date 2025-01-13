import streamlit as st
import os
import glob
from ast import literal_eval
import subprocess
import sys
import ctypes
import pandas as pd

# Import clara components
from clara.interpreter import getlanginter
from clara.parser import getlangparser
from clara.feedback import Feedback, FeedGen
from clara.feedback_python import PythonFeedback

path = os.getenv("LD_LIBRARY_PATH", "")
build_path = os.getenv("build_path", "")

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

def main():
    try:
        st.title("Clara Feedback Analysis")

        # Side Bar
        st.sidebar.subheader("List Problem")
        problem_type = st.sidebar.radio(
            "Select Problem",
            ["problemA", "problemB", "problemC", "problemD", "problemE", "problemF", "problemG", "problemH", "problemI", "problemJ"]
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
                ### Chef and Instant Noodles
                Chef has invented 1-minute Instant Noodles. As the name suggests, each packet takes exactly 1 minute to cook.

                Chef's restaurant has X stoves and only 1 packet can be cooked in a single stove at any minute.
                
                How many customers can Chef serve in Y minutes if each customer orders exactly 1 packet of noodles?

                ### Input Format
                - The first and only line of input contains two space-separated integers X and Y — the number of stoves and the number of minutes, respectively.

                ### Output Format
                - Print a single integer, the **maximum** number of customers Chef can serve in Y minutes

                ### Constraints
                - 1 ≤ X,Y ≤ 1000
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["3 7"],
                "Output": ["21"]
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

            st.write("""
                ### Explanation Sample 1
                Chef cooks for Y=7 minutes and can cook X=3 packets per minute, one on each stove.

                So, the total number of packets that can be cooked is X⋅Y=3⋅7=21.

                Each person orders one packet, so the maximum number of customers that can be served is 21.
            """)

            st.write("### Sample 2")
            data = {
                "Input": ["7 8"],
                "Output": ["56"]
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

            st.write("""
                ### Explanation Sample 2
                Chef cooks for Y=8 minutes and can cook X=7 packets per minute, one on each stove.

                So, the total number of packets that can be cooked is X⋅Y=7⋅8=56.

                Each person orders one packet, so the maximum number of customers that can be served is 56.
            """)

            args_input = "[[[1,2]], [[2,2]], [[3,7]], [[7,7]], [[7,8]], [[9,3]]]"
            type = "A"
        elif(problem_type == "problemB") :
            st.write("""
                ### Chef and Instant Noodles
                Currently there are courses for 4 languages, and hence there are 8 courses in this section. But suppose there are courses for N languages, what will be the total number of courses in this section?

                ### Input Format
                The only line of input will contain a single integer N, denoting the number of languages for which there are courses.

                ### Output Format
                Output on a single line the total number of courses in the section.

                ### Constraints
                - 1 ≤ X,Y ≤ 100
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["4"],
                "Output": ["8"]
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

            st.write("""
                ### Explanation Sample 1
                If there are 4 languages, then there will be 2∗4=8 courses in total.
            """)

            st.write("### Sample 2")
            data = {
                "Input": ["9"],
                "Output": ["18"]
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

            st.write("""
                ### Explanation Sample 2
                If there are 9 languages, then there will be 2∗9=18 courses in total.
            """)

            args_input = "[[2], [4], [5], [9], [12], [3]]"
            type = "B"
        elif(problem_type == "problemC") :
            st.write("""
                ### Alice and Marks
                Alice has scored X marks in her test and Bob has scored Y marks in the same test. Alice is happy if she scored at least twice the marks of Bob’s score. Determine whether she is happy or not.

                ### Input Format
                - The first and only line of input contains two space-separated integers X, Y — the marks of Alice and Bob respectively.

                ### Output Format
                For each testcase, print **Yes** if Alice is happy and **No** if she is not, according to the problem statement.

                ### Constraints
                - 1 ≤ X,Y ≤ 100
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["2 1"],
                "Output": ["Yes"]
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

            st.write("""
                ### Explanation Sample 1
                Alice has scored X = 2 marks whereas Bob has scored Y = 1 mark. As Alice has scored twice as much as Bob (i.e. X ≥ 2Y), the answer is **Yes**.
            """)

            st.write("### Sample 2")
            data = {
                "Input": ["1 2"],
                "Output": ["No"]
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

            st.write("""
                ### Explanation Sample 2
                Alice has scored X = 1 mark whereas Bob has scored Y = 2 marks. As Alice has not scored twice as much as Bob (i.e. X < 2Y), the answer is **No**.
            """)

            args_input = "[[[7, 9]], [[6, 6]], [[31, 53]], [[53, 8]], [[3, 8]]]"
            type = "C"
        elif(problem_type == "problemD") :
            st.write("""
                ### Chef and Brain Speed
                In ChefLand, human brain speed is measured in bits per second (bps). Chef has a threshold limit of X bits per second above which his calculations are prone to errors. If Chef is currently working at Y bits per second, is he prone to errors?

                If Chef is prone to errors print **YES**, otherwise print **NO**.

                ### Input Format
                The only line of input contains two space separated integers X and Y — the threshold limit and the rate at which Chef is currently working at.

                ### Output Format
                If Chef is prone to errors print **YES**, otherwise print **NO**.

                ### Constraints
                - 1 ≤ X,Y ≤ 100
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["7 9"],
                "Output": ["YES"]
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

            st.write("""
                ### Explanation Sample 1
                Chef's current brain speed of 9 bps is greater than the threshold of 7 bps, hence Chef is prone to errors.
            """)

            st.write("### Sample 2")
            data = {
                "Input": ["6 6"],
                "Output": ["NO"]
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

            st.write("""
                ### Explanation Sample 2
                Chef's current brain speed of 6 bps is not greater than the threshold of 6 bps, hence Chef is not prone to errors.
            """)
            st.write("### Sample 3")
            data = {
                "Input": ["31 53"],
                "Output": ["YES"]
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

            st.write("""
                ### Explanation Sample 3
                Chef's current brain speed of 53 bps is greater than the threshold of 31 bps, hence Chef is prone to errors.
            """)
            st.write("### Sample 4")
            data = {
                "Input": ["53 8"],
                "Output": ["NO"]
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

            st.write("""
                ### Explanation Sample 4
                Chef's current brain speed of 8 bps is not greater than the threshold of 53 bps, hence Chef is not prone to errors.
            """)

            args_input = "[[[2, 1]], [[1, 2]], [[8, 8]], [[53, 8]], [[3, 8]]]"
            type = "D"
        elif(problem_type == "problemE") :
            st.write("""
                ### Oneful Pairs
                Chef defines a pair of positive integers (a,b) to be a Oneful Pair, if

                a+b+(a⋅b)=111

                For example, (1,55) is a Oneful Pair, since 1+55+(1⋅55)=56+55=111.

                But (1,56) is not a Oneful Pair, since 1+56+(1⋅56)=57+56=113≠111.

                Given two positive integers a and b, output Yes if they are a Oneful Pair. And No otherwise.

                ### Input Format
                The only line of input contains two space-separated integers a and b.

                ### Output Format
                Output **Yes**, if (a,b) form a Oneful Pair. Output **No** if they do not.

                ### Constraints
                - 1 ≤ a, b ≤ 1000
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["1 55"],
                "Output": ["Yes"]
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

            st.write("""
                ### Explanation Sample 1
                (1,55) is a Oneful Pair, since 1+55+(1⋅55)=56+55=111.
            """)

            st.write("### Sample 2")
            data = {
                "Input": ["1 56"],
                "Output": ["No"]
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

            st.write("""
                ### Explanation Sample 2
                (1,56) is not a Oneful Pair, since 1+56+(1⋅56)=57+56=113≠111
            """)

            args_input = "[[[1, 55]], [[1, 56]], [[2, 35]], [[24, 2]], [[55, 1]], [[56, 1]]]"
            type = "E"
        elif(problem_type == "problemF") :
            st.write("""
                ### Positive and Negative
                Write a program to check whether a number given as user input is positive, negative, or zero.
            """)
            st.write("### Samples")
            data = {
                "Input": ["20", "0", "-95"],
                "Output": ["Positive", "Zero", "Negative"]
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

            args_input = "[[0], [-5], [10], [100], [-51]]"
            type = "F"
        elif(problem_type == "problemG") :
            st.write("""
                ### Grades of Student
                Write a program to print the grades of a student based on the marks he/she has obtained provided as input. The student is graded **A** if marks are greater than **90**, **B** if marks are greater than **70**, **C** if greater than or equal to **40**, else **F**.
            """)
            st.write("### Samples")
            data = {
                "Input": ["95", "40", "20"],
                "Output": ["A", "C", "F"]
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
            
            args_input = "[[0], [52], [10], [41], [40], [72], [70], [90], [92], [5]]"
            type = "G"
        elif(problem_type == "problemH") :
            st.write("""
                ### Print Squares
                Write a program that utilizes a while loop to print the squares of numbers from 1 to N.

                Check the sample input / output below further clarity
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["5"],
                "Output": ["1 4 9 16 25"]
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

            args_input = "[[5], [7], [10]]"
            type = "H"
        elif(problem_type == "problemI") :
            st.write("""
                ### Print factorial
                Write a program that uses a while loop to find the factorial of a given number.

                What is the Factorial of an integer N?

                A factorial is a function that multiplies a number by every number below it till 1.
                     
                For example, the factorial of 3 represents the multiplication of numbers 3, 2, 1, i.e. 3! = 3 × 2 × 1 and is equal to 6.

                Check sample input / output below for more clarity.

                ### Input Format
                There are multiple test files.

                Each input test file contains only 1 integer N.
                ### Output Format
                For each test file, output only the integer which is Factorial of N.
                
                You do not need to output anything else.
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["5"],
                "Output": ["120"]
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

            st.write("""
                ### Explanation Sample 1
                Factorial of 5 = 1 * 2 * 3 * 4 * 5 = 120
            """)

            args_input = "[[5], [7], [10]]"
            type = "I"
        elif(problem_type == "problemJ") :
            st.write("""
                ### Count Vowels

                Write a program that uses a while loop to find the number of vowels in a given input string of lowercase Latin letters.

                **Note**: Vowels in lowercase Latin letters are: `a`, `e`, `i`, `o`, and `u`.

                ### Input Format
                The only line of input contains a string.

                ### Output Format
                The only line of output contains a single integer - the count of vowels in the input string.
            """)
            st.write("### Sample 1")
            data = {
                "Input": ["codechef"],
                "Output": ["3"]
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

            st.write("""
                ### Explanation Sample 1
                codechef has 3 vowels: `o`, `e` and another `e`
            """)
        
            args_input = "[['codechef'], ['abcdefghijklmnopqrstuvwxyz'], ['codingpractice'], ['codingisfun']]"
            type = "J"

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
            st.code(incorrect_program.getvalue().decode("utf-8"), language="python")

        # Cluster directory input
        cluster_dir = os.path.join(os.path.dirname(__file__), 'clusters')
        cluster_dir = os.path.join(cluster_dir, type)

        max_cost = 0 #0 means no limit
        clean_strings = False #Clean Strings
        ignore_io = True #Input Output
        ignore_ret = False #Return Value

        if st.button("Generate Feedback", type="primary"):
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
                            st.success("Feedback generated successfully!")
                            st.subheader("Feedback:")
                            for f in feedback.feedback:
                                st.markdown(f"* {f}")
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