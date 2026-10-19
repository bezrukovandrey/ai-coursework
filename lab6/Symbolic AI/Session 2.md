
# Revision/Recap

![[Pasted image 20251112081641.png]]

![[Pasted image 20251112081702.png]]

![[Pasted image 20251112081722.png]]


# Lecture

## Horn clause

![[Pasted image 20251112082010.png]]

If my formula is made up of only horn clauses then we can solve the equation in polynomial time => it will be much faster

![[Pasted image 20251112082253.png]]

### Forward Chaining algorithm

![[Pasted image 20251112083129.png]]

![[Pasted image 20251112083146.png]]

![[Pasted image 20251112083204.png]]


### Backward Chaining algorithm

![[Pasted image 20251112085113.png]]

In Forward chaining we calculate all the statements and we deduce everything to be deduced. 

With backward chaining, due to its recursive nature, we only calculate what needs to be calculated. We ignore redundant statements. In this example Forward and Backward chaining result in the same calculations.

![[Pasted image 20251112085429.png]]

In this example we will loop forever since if we want to evaluate `z` we need to evaluate `x`, but `x` relies on `z` so it is gonna recurse forever.

To solve this problem we can create a global array that keeps track of variables that we already evaluated:



![[Pasted image 20251112090558.png]]

![[Pasted image 20251112091445.png]]

