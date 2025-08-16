import openai

openai.api_key = ' '
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.5,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {e}"
