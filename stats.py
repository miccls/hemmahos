from hemmahos import FHR
from matplotlib import pyplot as plt

if __name__ == '__main__':
        
    schd = FHR("form.csv", 3)

    sample_nums = [10, 100, 1000, 10000, 100000, 500000]
    scores = []
    for num in sample_nums:
        best_schd = schd.sample(num)
        scores.append(best_schd['score'])

    plt.plot(sample_nums, scores)
    plt.show()