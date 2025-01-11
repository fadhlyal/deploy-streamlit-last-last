import streamlit as st
import os
import glob
from ast import literal_eval
import subprocess
import sys
import ctypes

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
            ["problemA", "problemB"]
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
            args_input = "[[[1,2]], [[2,2]], [[3,7]], [[7,7]], [[7,8]], [[9,3]]]"
            type = "A"
        elif(problem_type == "problemB") :
            args_input = "[[2], [4], [5], [9], [12], [3]]"
            type = "B"
        elif(problem_type == "problemC") :
            args_input = "[[[7, 9]], [[6, 6]], [[31, 53]], [[53, 8]], [[3, 8]]]"
            type = "C"
        elif(problem_type == "problemD") :
            args_input = "[[[2, 1]], [[1, 2]], [[8, 8]], [[53, 8]], [[3, 8]]]"
            type = "D"
        elif(problem_type == "problemE") :
            args_input = "[[[1, 55]], [[1, 56]], [[2, 35]], [[24, 2]], [[55, 1]], [[56, 1]]]"
            type = "E"

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
        ignore_io = False #Input Output
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