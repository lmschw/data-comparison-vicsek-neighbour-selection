import matplotlib.pyplot as plt
import Animator

class Animator2D(Animator.Animator):
    """
    Animator class for 2D graphical representation.
    """

    def __init__(self):
        """
        Constructor. Returns the Animator2D instance.
        """
        self.setParameters()

    def _animate(self, i):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """

        plt.clf()
        plt.quiver(self._positions[i,:,0],self._positions[i,:,1],self._orientations[i,:,0],self._orientations[i,:,1],color=self._colours[i])
        plt.xlim(0,self._domainSize[0])
        plt.ylim(0,self._domainSize[1])
        if self._showParameters:
            plt.title(f"n={self._n}, k={self._k}, noise={self._noise}, radius={self._radius}, speed={self._speed}, \nneighbour selection={self._neighbourSelectionMode}\n$t$={self._time[i]:.2f}")
        else:
            plt.title(f"$t$={self._time[i]:.2f}")