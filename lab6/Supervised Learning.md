
*Input (Data):*  ($x^{(1)}$,$y^{(1)}$),...,($x^{(i)}$,$y^{(i)}$),...,($x^{(n)}$,$y^{(n)}$)    

$x^{(1)}$: a vector of features/variables
$y^{(1)}$: the answer associated to $x^{(1)}$

Output: given a new $x^{(0)}$, return $y^{(0)}$ associated with $x^{(0)}$

$x^{(0)}$ != $x^{(i)}$ for all 1 <= i <= n

Example: ($Student^{(i)}$,$Salary^{(i)}$)

$Student^{(i)}$ = (Number of education years, seniority)


### Linear Regression

$y^{(i)}$ = h ($x^{(i)}$) + $\epsilon^{(i)}$  1 <= i <= n

Find h

$x^{(i)}$ = ($x_1^{(i)}$,$x_2^{(i)}$,$x_3^{(i)}$,...,$x_d^{(i)}$) $\in$ $\mathbb{R}^d$  
$y^{(i)} \in$ $\mathbb{R}$

Assumption: h is a linear function: $\mathbb{R}^d\to\mathbb{R}$ 

h(x) = $\theta_0$ + $\theta_1x_1$+ $\theta_2x_2$ + ... + $\theta_dx_d$    

Finding h is equivalent to finding $\theta_0$ + $\theta_1x_1$+ $\theta_2x_2$ + ... + $\theta_dx_d$
x = ($x_1$,...,$x_d$) $\to$ (1,$x_1$,$x_2$,...,$x_d$)

h(x) = <$\theta$,x> where $\theta$ = ($\theta_0$,$\theta_1$,...,$\theta_d$)
= $\theta.x$       x = (1,$x_1$,...,$x_d$)

![[Pasted image 20250917082820.png]]
![[Pasted image 20250917083348.png]]


Find $\theta$ such that
	J($\theta$) = $\sum_{i=1}^n$ ($y^{(i)}$ - <$\theta$,$x^{(i)}$>)$^2$ is minimized
Objective: min J($\theta$)

#### Gradient Descent:

f: $\mathbb{R}^d\to\mathbb{R}$

$\nabla f(x)$ = ($\frac{{d} f(x)}{{d} x_1}$,$\frac{{d} f(x)}{{d} x_2}$,...,$\frac{{d} f(x)}{{d} x_d}$)

1. Start at same arbitrary $z^0$
2. Repeat
	$z^{(t+1)}$ $\leftarrow$ $z^t$ - $\alpha^t.\nabla f(z^t)$  
	$\alpha^t$ is the step size
	$\nabla f(z^t)$ is the gradient of f at $z^t$
	until time T such that || $\nabla f(z^t)$ || $\leq$ $\epsilon$ 

$\nabla J(\theta)$:

$\frac{{d}J(\theta)}{{d}\theta_1}$ = $\sum_{i=1}^n$ $\frac{{d}}{{d}\theta_1}$\[($y^{(i)}$ - <$\theta$,$x^{(i)}$>)$^2$]

= $\sum_{i=1}^n$ 2($y^{(i)}$ - <$\theta$,$x^{(i)}$>).$\frac{{d}}{{d}\theta_1^{-}}$<$\theta$,$x^{(i)}$>
= $\sum_{i=1}^n$ 2($y^{(i)}$ - <$\theta$,$x^{(i)}$>).($-x_1^{(i)}$) 

$\nabla J(\theta)$ = ($\frac{{d}J(\theta)}{{d}\theta_0}$,$\sum_{i=1}^n$ 2($y^{(i)}$ - <$\theta$,$x^{(i)}$>).($-x_1^{(i)}$), ... , $\sum_{i=1}^n$ 2($y^{(i)}$ - <$\theta$,$x^{(i)}$>).($-x_d^{(i)}$))

> Exercise for you: try to do $\frac{{d}J(\theta)}{{d}\theta_0}$ yourself


*Remarks:*

1. Step size $\alpha^t$ ~ O($\frac{1}{\sqrt{t}}$)
![[Pasted image 20250917085846.png]]

> if we have a large step size we will jump over the optimal point and keep going back and forth converging to it, so we need a to decrease the step size when we get close to ot.


#### Probabilistic explanation

$y^{i}$ = $\theta.x^{(i)} +\epsilon^{(i)}$

here $\theta$ is the unknown 

*Observation:* $\epsilon^{(i)}$ ~ N(0,$\sigma^2$)
![[Pasted image 20250917090556.png]]

Density function: P($\epsilon^{(i)}$) = $\frac{1}{\sqrt{2\pi\sigma}}$.$e^{\frac{\epsilon^{(i)^2}}{2\sigma^2}}$

P($\epsilon^{(i)}$) = $\frac{1}{\sqrt{2\pi\sigma}}$. $e^{-\frac{[y^{(i)}-\theta.x^{(i)}]^2}{2\sigma^2}}$

Error on data i is P($\epsilon^{(i)}$)

Likely-hood function: $\prod_{i=1}^{n}$ P($\epsilon^{(i)}$)

*Objective:* find $\theta$ such that we get the max likely-hood

max $\prod_{i=1}^{n}$ P($\epsilon^{(i)}$)

<=> max $\prod_{i=1}^{n}$ $\frac{1}{\sqrt{2\pi\sigma}}$. $e^{-\frac{[y^{(i)}-\theta.x^{(i)}]^2}{2\sigma^2}}$

<=> max ($\frac{1}{\sqrt{2\pi\sigma}}$)$^n$ . $e^{-\frac{[y^{(i)}-\theta.x^{(i)}]^2}{2\sigma^2}}$

<=> max$\theta$ - $\sum_{i=1}^n$ \[$y^{(i)} -\theta.x^{(i)}$]$^2$

<=> min$\theta$ $\sum_{i=1}^n$ \[$y^{(i)} -\theta.x^{(i)}$]$^2$



