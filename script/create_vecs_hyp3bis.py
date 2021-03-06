#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.vectorise as vutils
import utils.function as futils
import utils.preprocess as putils


def pp(str0):
    return putils.tokenise(putils.convert_to_lowercase(str0))


def get_label_col(index, var):
    return [v[index] for v in var]


def hyp3_pp(ds):
    return[pp(rp) for rp in get_label_col(3, ds)]


def create_objType(ds):
    return [int(x[0] == x[1]) for x in ds]


def add_objType_to_vec(vecs, objType):
    return [vec + [x] for vec, x in zip(vecs, objType)]


def add_source_to_vecs(tweets, sources, vecs):
    del sources
    tv = {t: v for t, v in zip(tweets, vecs)}
    ts = futils.open_json("../dataset/traindev/direct_structures.json")
    return [v + tv[ts.get(t, t)] for t, v in zip(tweets, vecs)]


def main():
    print("Extraction")
    lTrain = futils.open_json("../dataset/my_datasets/train.json")
    lDev = futils.open_json("../dataset/my_datasets/dev.json")
    tweets_train = get_label_col(0, lTrain)
    tweets_dev = get_label_col(0, lDev)
    sources_train = get_label_col(1, lTrain)
    sources_dev = get_label_col(1, lDev)
    objType_train = create_objType(lTrain)
    objType_Dev = create_objType(lDev)
    print("Preprocessing")
    lTrain = hyp3_pp(lTrain)
    lDev = hyp3_pp(lDev)
    print("Vectorisation")
    lTrain, all_words = vutils.vectorise_train(lTrain)
    lDev = vutils.vectorise_test(lDev, all_words)
    lTrain = add_objType_to_vec(lTrain, objType_train)
    lDev = add_objType_to_vec(lDev, objType_Dev)
    lTrain = add_source_to_vecs(tweets_train, sources_train, lTrain)
    lDev = add_source_to_vecs(tweets_dev, sources_dev, lDev)

    print("Saving")
    futils.create_json("../dataset/my_datasets/hyp3bis_train_vecs.json",
                       lTrain)
    futils.create_json("../dataset/my_datasets/hyp3bis_dev_vecs.json",
                       lDev)


if __name__ == '__main__':
    main()
