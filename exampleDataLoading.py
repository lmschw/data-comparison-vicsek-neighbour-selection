import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

"""
--------------------------------------------------------------------------------
PURPOSE 
Loads a saved model and creates a video.
--------------------------------------------------------------------------------
"""

datafileLocation = ""
filename = "test_event_noise=100_local_1e_switchType=MODE_ordered_st=F_o=F_do=N_d=0.09_n=225_r=10_k=1_noise=1_drn=1000_5000-align_noise_1"
modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=True)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=15000)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation(f"{filename}.mp4")

# Display Animation
#preparedAnimator.showAnimation()