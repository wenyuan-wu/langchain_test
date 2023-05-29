from dotenv import load_dotenv
from reason_finder import get_full_info, create_context_template, reason_extractor

history = ['patient: Hi', 'physician: Hello! How can I assist you today?']
contex = """The patient's name is Daniel and he is 34 years old with a BMI of 27. His plan includes intermittent 
fasting with an eating window until 1 pm and swimming for 30 minutes or 500 meters on Monday, Thursday, and Saturday 
evenings. The measure he was supposed to take was to go swimming on Thursday evening, but the {'completed': false} 
indicates that he did not do it as intended."""

reason = reason_extractor(contex, history)
print(reason)
