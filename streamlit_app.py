import streamlit as st


def main():
    st.title("Simple Greeting App")

    # Get user input for name
    name = st.text_input("Enter your name:")

    # Display the greeting message
    if name:
        st.write(f"Hello, {name}!")


if __name__ == "__main__":
    main()




