from utils import calculate_similarity

if __name__=="__main__":
    resume = input("Paste resume text:\n")
    jd = input("Paste job description:\n")

    score = calculate_similarity(resume, jd)

    print(f"\nMatch Score: {score}%")