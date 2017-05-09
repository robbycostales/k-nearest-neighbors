# known format: list([[12d vector], id]))
# "songs to classify" format is the same
import copy
import numpy as np
import statistics
import itertools
import operator


def most_common(L):
    """
    Returns most frequent element in the data set
    If tie, returns the value with first appearence

    Args:
        L : data

    Returns:
        most frequent value
    """
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item
        def _auxfun(g):
            item, iterable = g
            count = 0
            min_index = len(L)
            for _, where in iterable:
                count += 1
                min_index = min(min_index, where)
            # print 'item %r, count %r, minind %r' % (item, count, min_index)
            return count, -min_index
    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]


def magnitude(vector):
    """
    Finds the magnitude of a vector
    ( or euclidean distance between vector and origin )

    Args:
        vector : vector

    Returns:
        magnitude
    """
    total = 0
    for i in vector:
        total += i**2
    total = total ** (1/2)
    # function is complete
    return total


def similarity(a, b):
    """
    Determines how "similar", or close two vectors are
    Is essentially: 1 - cosine distance

    Args:
        a : vector  1
        b : vector  2

    Returns:
        Value between 0 and 1
        1 = very far away
        0 = very close (most similar)
    """
    # function is complete
    return 1 - (np.dot(a, b) / (magnitude(a) * magnitude(b)))


def k_nearest_neighbors(original, new, k, names, printing):
    """
    Determines accuracy of the selections made by the k nearest neighbors
    algorithm

    Will also tell us how good our original data is at being sorted into
    clusters

    Args:
        original : original data points - will be used for determining the
                    status of new points
        new : new points to be classified
        k : number of points in radius considered
        names : list of names where each index corresponds to the id's of the
                points
        printing: boolean that determines whether or not printing of results
                    will take place

    Returns:
        percentage of points that were correctly identified
        value between 0 and 1
    """

    # for individual composer data
    total_pieces_by_composer = [0 for i in range(len(names))]
    correct_pieces_by_composer = [0 for i in range(len(names))]

    total_new_points = len(new)
    # at end, num_correct / total_new_points will be the accuracy value
    num_correct = 0

    # for each point in the points to be classified
    for item in new:
        point = item[0]
        point_id = item[1]

        # find all distances between "point", and the original data points
        data = copy.deepcopy(original)
        # each element in data has:
        # [[vector values], id]

        for element in data:
            element.append(similarity(point, element[0]))
        # each element in data has:
        # [[vector values], id, similarity to point]

        # sorts data by 3rd value (second index) of element
        data_sorted = sorted(data, key=operator.itemgetter(2))

        # the k closest vectors' classiciations
        k_classifications = []
        for i in range(k)
            # append the id of the ith element in data_sorted
            k_classiciations.append(data_sorted[i][1])

        classification = most_common(k_classifications)
        # if we get the correct classiciation
        if classiciation == point_id:
            num_correct += 1
            correct_pieces_by_composer[point_id] += 1
        total_pieces_by_composer[point_id] += 1


    accuracy = num_correct / total_new_points
    # if printing option is True:
    if printing:
        print("\n\n# Original Data : {0}".format(len(original)))
        print("# To Be Classified : {0}\n".format(len(new)))
        print("# Correctly Identified : {0} / {1}".format(num_correct, len(new)))
        print("Accuracy : {0}\n".format(accuracy))

        print("{0:<8}{1:<8}{2:<8}{3:<8}".format("Names", "Num Correct",
                                                "Total", "Accuracy")
        for i in range(len(names)):
            # Format:
            # Composer:
            print("{0:<10}{1:<10}{2:<10}{3:<10}".format(names[i],
                correct_pieces_by_composer[i], total_pieces_by_composer[i],
                correct_pieces_by_composer[i] / total_pieces_by_composer[i])

    # function is complete
    return accuracy


def determine_k(original, new):
    """
    Determines which k is best suited for the nearest neighbors algorithm
    based on accuracy of results

    Args:
        original : original data points - will be used for determining the
                    status of new points
        new : new points to be classified

    Returns:
        best suited k
    """
    optimal = 0
    optimal_k = 0
    for k in range(len(original)):
        accuracy = k_nearest_neighbors(original, new, k, False)
        # if the new accuracy value is greater for this k than previously,
        # update k
        if accuracy > optimal:
            optimal = accuracy
            optimal_k = k

    # function is complete
    return optimal_k
