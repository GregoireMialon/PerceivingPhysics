auth: Craig Wm. Versek (cversek@gmail.com) 
dates: gist created 2016/06/09 based directly from code written circa 2008 while I was a PhD candidate at UMass Amherst

These are simple `pygame` based pendulum physics simulations that started with a simple idea: perform the numerical integration (the "physics") within an infinite generator loop, supplying the parameters to the graphics rendering code on demand.  The thought was to separate the number crunching from the application at large and simplify its organization and portability.  The code can be configured to use one of a few numerical integration methods by swapping generators with the same interface. `pygame` is the only dependency that needs to be installed.

`phys_gen.py` illustrates the basic concept with no bells & whistles (nor graphics).

`pendulum.py` is a pygame driven simple pendulum interactive simulation -- try clicking and dragging the bob. Can use Heun, Steormer_Verlet, or RK4 methods. 

`doubled_pedulum.py` has two double pendula running in tandem with very close but not equal initial conditions. Can use RK4 or Steormer_Verlet methods. Note, the physical system is chaotic and *should* conserve energy, but numerical integration errors build up and the behavior tends towards a mode of the small angle approximation.  Some day this needs to be put right!