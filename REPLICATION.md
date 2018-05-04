# START HERE!

## How to follow instructions

I've gone through and made sure this can be pasted in as is. 

Please feel free to do just that

## Setup Env

Using Python 3.6.5 :: Anaconda, Inc.

`conda config --append channels chroxvi`
`conda create -n ryan_ds_challenge --file requirements.txt`
`source activate ryan_ds_challenge`

## Problem 1:


For both notebooks just run all of the cells

See response_times_scenario1.ipynb
See response_times_scenario2.ipynb

if you'd rather look at .html...

See response_times_scenario1.html
See response_times_scenario2.html



## Problem 2:

Pretty much just follow the notebook, it's straight forward. 

Problem2.ipynb

If you'd rather not...

## (optional) Running from command line

#### Time complexity results

`python -m cProfile -o time_profile_run_by_user.prof utils.py`
`snakeviz time_profile_run_by_user.prof`

#### Space complexity results

`python -m memory_profiler utils.py`

#### Finally: You'll still have to look at the writeup in the notebook for my comments on Time and Space complexity

If you won't do this in Jupyter 

look at the Problem2.html file created from the notebook

