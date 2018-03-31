# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    clause1 = logic.disjoin(A, B)
    clause2 = ~A % logic.disjoin(~B, C)
    clause3 = logic.disjoin(~A, ~B, C)
    return logic.conjoin(clause1, clause2, clause3)

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    clause1 = C % logic.disjoin(B, D)
    clause2 = A >> (logic.conjoin(~B, ~D))
    clause3 = (~(logic.conjoin(B, ~C)) >> A)
    clause4 = (~D) >> C
    return logic.conjoin(clause1, clause2, clause3, clause4)


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    Alive_1 = logic.PropSymbolExpr("WumpusAlive[1]")
    Alive_0 = logic.PropSymbolExpr("WumpusAlive[0]")
    Born_0 = logic.PropSymbolExpr("WumpusBorn[0]")
    Killed_0 = logic.PropSymbolExpr("WumpusKilled[0]")
    clause1 = Alive_1 % (logic.disjoin(logic.conjoin(Alive_0,(~Killed_0)),(logic.conjoin((~Alive_0),Born_0))))
    clause2 = ~(logic.conjoin(Alive_0,Born_0))
    clause3 = Born_0
    return logic.conjoin(clause1, clause2, clause3)


def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    clause = logic.to_cnf(sentence)
    result = logic.pycoSAT(clause)
    return result


def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    return logic.disjoin(literals)

def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    final_literals = []
    non_literals = []
    for i in range(len(literals)):
        non_literals.append(~literals[i])
    for i in range(len(non_literals)):
        for j in range(i+1, len(non_literals)):
            clause = logic.disjoin(non_literals[i], non_literals[j])
            final_literals.append(clause)
    return logic.conjoin(final_literals)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    final_literals = [logic.disjoin(literals)]
    non_literals = []
    for i in range(len(literals)):
        non_literals.append(~literals[i])
    for i in range(len(non_literals)):
        for j in range(i+1, len(non_literals)):
            clause = logic.disjoin(non_literals[i], non_literals[j])
            final_literals.append(clause)
    return logic.conjoin(final_literals)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    action_string = []
    # print model.keys()
    # print (len(model))
    # print model.keys()[0]
    # print model[0]
    parse_strings = [logic.PropSymbolExpr.parseExpr(sym_string) for sym_string in model.keys() if model[sym_string] == True]
    for parse_string in parse_strings:
        # print(parse_string[0])
        if parse_string[0] in actions:
            action_string.append(parse_string)
    tmp_result = sorted(action_string, key=lambda x: int(x[1]))
    return [tmp_result[i][0] for i in range(len(tmp_result))]

def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    # print(walls_grid)
    now_pos = logic.PropSymbolExpr(pacman_str, x, y, t)
    x_pos = [x-1, x+1]
    y_pos = [y-1, y+1]

    prev_poses = []
    for new_x in x_pos:
        if walls_grid[new_x][y] == False:
            prev_position = logic.PropSymbolExpr(pacman_str, new_x, y, t-1)
            prev_action = logic.PropSymbolExpr('East', t-1) if new_x == x-1 else logic.PropSymbolExpr('West', t-1)
            prev_poses.append(logic.conjoin(prev_position, prev_action))

    for new_y in y_pos:
        if walls_grid[x][new_y] == False:
            prev_position = logic.PropSymbolExpr(pacman_str, x, new_y, t-1)
            prev_action = logic.PropSymbolExpr('North', t-1) if new_y == y-1 else logic.PropSymbolExpr('South', t-1)
            prev_poses.append(logic.conjoin(prev_position, prev_action))
    # print(now_pos % logic.disjoin(prev_poses))
    return(now_pos % logic.disjoin(prev_poses))


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    # print(walls)
    # print(walls.asList())
    time_limit = 50
    start_state = problem.getStartState()
    (start_x, start_y) = start_state
    goal_state = problem.getGoalState()
    (goal_x, goal_y) = goal_state
    actions = ['East', 'West', 'North', 'South']
    start_expr = logic.PropSymbolExpr(pacman_str, start_x, start_y, 0)
    pos_limit = []
    act_limit = []
    wall_limit = []
    for i in range(time_limit):
        for x1 in range(1, width+1):
            for y1 in range(1, height+1):
                for x2 in range (x1, width+1):
                    for y2 in range(1, height+1):
                        if x1 != x2 or y1 != y2:
                            con_pos1 = logic.PropSymbolExpr(pacman_str, x1, y1, i)
                            con_pos2 = logic.PropSymbolExpr(pacman_str, x2, y2, i)
                            con_pos_clause = logic.Expr("~", logic.conjoin(con_pos1, con_pos2))
                            pos_limit.append(con_pos_clause)
        pos_limit_expr = logic.conjoin(pos_limit)
        # print(pos_limit_expr)
        for action1 in actions:
            for action2 in actions:
                if action1 != action2:
                    con_act1 = logic.PropSymbolExpr(action1, i)
                    con_act2 = logic.PropSymbolExpr(action2, i)
                    con_act_clause = logic.Expr("~", logic.conjoin(con_act1, con_act2))
                    act_limit.append(con_act_clause)
        act_limit_expr = logic.conjoin(act_limit)
        # print(act_limit_expr)
        for xx in range(1, width + 1):
            for yy in range(1, height + 1):
                if (xx, yy) not in walls.asList():
                    wall_limit.append(pacmanSuccessorStateAxioms(xx, yy, i + 1, walls))
        wall_limit_expr = logic.conjoin(wall_limit)
        # print(wall_limit_expr)
        goal_expr = logic.PropSymbolExpr(pacman_str, goal_x, goal_y, i)
        final_clause = logic.conjoin(pos_limit_expr,act_limit_expr,act_limit_expr,wall_limit_expr,goal_expr,start_expr)
        result = findModel(final_clause)
        if result is not False:
            # print (extractActionSequence(result, actions))
            return extractActionSequence(result, actions)


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    time_limit = 50
    start_state = problem.getStartState()[0]
    (start_x, start_y) = start_state
    food_lists = problem.getStartState()[1].asList()
    # print(food_lists)
    actions = ['East', 'West', 'North', 'South']
    start_expr = logic.PropSymbolExpr(pacman_str, start_x, start_y, 0)
    pos_limit = []
    act_limit = []
    wall_limit = []
    for i in range(time_limit):
        for x1 in range(1, width+1):
            for y1 in range(1, height+1):
                for x2 in range (x1, width+1):
                    for y2 in range(1, height+1):
                        if x1 != x2 or y1 != y2:
                            con_pos1 = logic.PropSymbolExpr(pacman_str, x1, y1, i)
                            con_pos2 = logic.PropSymbolExpr(pacman_str, x2, y2, i)
                            con_pos_clause = logic.Expr("~", logic.conjoin(con_pos1, con_pos2))
                            pos_limit.append(con_pos_clause)
        pos_limit_expr = logic.conjoin(pos_limit)
        # print(pos_limit_expr)
        for action1 in actions:
            for action2 in actions:
                if action1 != action2:
                    con_act1 = logic.PropSymbolExpr(action1, i)
                    con_act2 = logic.PropSymbolExpr(action2, i)
                    con_act_clause = logic.Expr("~", logic.conjoin(con_act1, con_act2))
                    act_limit.append(con_act_clause)
        act_limit_expr = logic.conjoin(act_limit)
        # print(act_limit_expr)
        for xx in range(1, width + 1):
            for yy in range(1, height + 1):
                if (xx, yy) not in walls.asList():
                    wall_limit.append(pacmanSuccessorStateAxioms(xx, yy, i + 1, walls))
        wall_limit_expr = logic.conjoin(wall_limit)
        # print(wall_limit_expr)
        total_food_limit =[]
        for food in food_lists:
            one_food_limit = []
            for t in range(i+1):
                one_food_limit.append(logic.PropSymbolExpr("P", food[0], food[1], t))
            one_food_eat_expr = logic.disjoin(one_food_limit)
            total_food_limit.append(one_food_eat_expr)
        food_limit_expr = logic.conjoin(total_food_limit)
        final_clause = logic.conjoin(pos_limit_expr,act_limit_expr,act_limit_expr,wall_limit_expr,start_expr,food_limit_expr)
        result = findModel(final_clause)
        if result is not False:
            # print (extractActionSequence(result, actions))
            return extractActionSequence(result, actions)


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# print (findModel(sentence1()))

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)


