# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  from util import Stack  

  stack = Stack()
  visited = set()

    
  stack.push( ( problem.getStartState(), [] ) )

  while not stack.isEmpty():
        state, path = stack.pop() 

        if problem.isGoalState(state):
            return path

        if state not in visited:
            visited.add(state)

            for successor, action, stepCost in problem.getSuccessors(state):
                new_path = path + [action]
                stack.push((successor, new_path))

 # print("Start:", problem.getStartState())
  #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
  #print("Start's successors:", problem.getSuccessors(problem.getStartState()))  

  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  from util import Queue

  queue = Queue()
  visited = set()

  queue.push((problem.getStartState(), []))

  while not queue.isEmpty():
     state, path = queue.pop()

     if problem.isGoalState(state):
        return path
     
     if state not in visited:
        visited.add(state)

        for successor, action, stepCost in problem.getSuccessors(state): # to add stepCost later
           new_path = path + [action]
           queue.push((successor, new_path))
  
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  from util import PriorityQueue

  pr_q = PriorityQueue()
  visited = set()

  pr_q.push((problem.getStartState(), [], 0), 0)

  while not pr_q.isEmpty():
     state, path, cost_so_far = pr_q.pop()

     if problem.isGoalState(state):
        return path
     
     if state not in visited:
        visited.add(state)

        for successor, action, step_cost in problem.getSuccessors(state):
           new_cost = cost_so_far + step_cost
           new_path = path + [action]
           pr_q.push((successor, new_path, new_cost), new_cost)

  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

# def aStarSearch(problem, heuristic=nullHeuristic):
#   "Search the node that has the lowest combined cost and heuristic first."
#   "*** YOUR CODE HERE ***"
#   from util import PriorityQueue
#   import itertools #added to introduce a tie breaker, making entries unique even if priorities tie

#   pr_q = PriorityQueue()
#   visited = set()
#   counter = itertools.count()

#   start_state = problem.getStartState()
#   start_cost = heuristic(start_state, problem)

#   pr_q.push((start_state, [], 0, next(counter)), start_cost)

#   while not pr_q.isEmpty():
#      state, path, cost_so_far, _ = pr_q.pop()

#      if problem.isGoalState(state):
#         return path
     
#      if state not in visited:
#         visited.add(state)

#         for successor, action, step_cost in problem.getSuccessors(state):
#            new_cost = cost_so_far + step_cost
#            new_path = path + [action]
           
#            priority = new_cost + heuristic(successor, problem)

#            pr_q.push((successor, new_path, new_cost, next(counter)), priority)

#   util.raiseNotDefined()
    
def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost (g + h) first.
    Works for any consistent heuristic.
    """
    from util import PriorityQueue
    import itertools

    # Priority queue to select the node with smallest f = g + h
    pr_q = PriorityQueue()
    visited = set()
    counter = itertools.count()  # Used to break ties (avoid comparison errors)

    start_state = problem.getStartState()
    start_cost = 0
    start_priority = start_cost + heuristic(start_state, problem)

    # Push initial node: (state, path_so_far, total_cost)
    pr_q.push((start_state, [], start_cost), (start_priority, next(counter)))

    while not pr_q.isEmpty():
        state, path, cost_so_far = pr_q.pop()

        # Check goal condition
        if problem.isGoalState(state):
            return path

        # Only expand unvisited states
        if state not in visited:
            visited.add(state)

            # Explore all successors
            for successor, action, step_cost in problem.getSuccessors(state):
                new_cost = cost_so_far + step_cost
                new_path = path + [action]
                priority = new_cost + heuristic(successor, problem)
                pr_q.push((successor, new_path, new_cost), (priority, next(counter)))

    # If somehow no path found
    return []

#util.raiseNotDefined()

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
