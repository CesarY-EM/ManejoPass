from utils import utils
from streamlit.web import cli as stcli
import streamlit as st
import sys

def main():
    utils.main()

if __name__ == "__main__":
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())