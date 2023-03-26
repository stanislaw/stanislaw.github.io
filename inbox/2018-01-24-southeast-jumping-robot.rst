A Southeast Jumping Robot: Notes on one proof from a textbook
=============================================================

:date: 2018-01-28 17:20:00
:modified: 2018-01-28 17:20:00
:tags: Math
:category: Posts
:slug: 2018-01-24-southeast-jumping-robot
:summary: Short summary

.. raw:: html

    <style type="text/css">
    .math-block {
      font-family: monospace;
      white-space: pre;
      /*font-weight: bolder;*/
      font-size: 18px;
      margin: 10px;
      padding: 5px 10px;
      background-color: #efeefe;
    }
    .math-inline {
      font-family: monospace;
      /*font-weight: bolder;*/
      font-size: 18px;
      /*margin: 10px;*/
      padding: 1px 5px;
      background-color: #efeefe;
    }
    </style>

    <a name="intro" href="#intro"></a>

.. _Introduction:

Introduction
------------

This ad-hoc post is dedicated to one small proof from a textbook "Mathematics
for Computer Science" [[1](#anchor_01_mathematics)] which is a recommended
reading in the course "Formal Software Verification" [[2]](#anchor_02_course).
It took a while for me to understand the reasoning behind this proof so I
decided to share my experience in a blog post because I did not find any
information about it on the internet. Hopefully it will help someone who
is working with this textbook to understand the material better.

My goal is to fill in the details I missed in the textbook, not to give a
complete explanation of a problem so it is most likely that this post will only
make sense to those who are familiar with the context of this proof: the chapter
called "6.3 Partial Correctness & Termination".

- `Introduction <Introduction2>`_
- [A Southeast Jumping Robot: Contrived example of a termination proof](#robot)
- [Understanding the problem](#understanding-problem)
- [Proof](#proof)
  - [1. Proof of the lemma 2.4.6](#proof-1)
  - [2. Proof that `v` is a strictly decreasing derived variable](#proof-2)
  - [3. Implication of Theorem 6.3.3: Robot always gets stuck.](#proof-3)
- [Geometric interpretation](#geometric-interpretation)
- [Credits](#credits)
- [Links](#links)

<a name="robot" href="#robot"></a>

## A Southeast Jumping Robot

This proof is located in section "6.3.4 A Southeast Jumping Robot (Optional)",
page 180 of the book and page 188 of a textbook. It proves the following claim:

> Claim 6.3.4. The robot will always get stuck at the origin.

The following is a direct quote from a textbook:

<img src="/images/2018-01-24-southeast-jumping-robot/ASouthEastJumpingRobotIntro.png"/>

<a name="understanding-problem" href="#understanding-problem"></a>

## Understanding the problem

> Claim 6.3.4. The robot will always get stuck at the origin.

The key observation about the behaviour of the robot is that even though the
robot can jump East quicker than West, sooner or later it will not be able to
jump East when it reaches the bottom of the quadrant due to the `y - 1`
component of the Southeast move. After the robot has reached the bottom of the
quadrant it can only move West so finally it will get stuck in `(0, 0)`
because the West move will also become impossible.

## Proof

This is the proof that the textbook suggests:

<img src="/images/2018-01-24-southeast-jumping-robot/ASouthEastJumpingRobotProof.png"/>

Let's consider three building blocks of this proof:

1) Lemma 2.4.6

2) Show that `𝑣` is strictly decreasing i.e. show the implication:

<div class="math-block">(𝑥, 𝑦) ⟶ (𝑥', 𝑦') ⟹ 𝑣((𝑥', 𝑦')) < 𝑣((𝑥, 𝑦))
</div>

3) Show the implication from Theorem 6.3.3 that Robot always get stuck.

<a name="proof-1" href="#proof-1"></a>

### 1. Proof of the lemma 2.4.6

Let's look the lemma up in the textbook:

<img src="/images/2018-01-24-southeast-jumping-robot/Lemma-2.4.6-Proof.png"/>

> Lemma 2.4.6. ℕ + 𝔽&nbsp; is well ordered.

The definition of `ℕ + 𝔽` requires us to understand what is 𝔽 first:

<img src="/images/2018-01-24-southeast-jumping-robot/Definition-Set-F.png"/>

This is the definition of **well-ordered** by Wikipedia:

> In mathematics, a well-order (or well-ordering or well-order relation) on a set
S is a total order on S with the property that every non-empty subset of S has a
least element in this ordering. The set S together with the well-order relation
is then called a well-ordered set.

**The Well Ordering Principle** is defined at the start of chapter 2: "Well
Ordering Principle" as

> Every nonempty set of nonnegative integers has a smallest element.

> While the Well Ordering Principle may seem obvious, it’s hard to see offhand why it is useful. But in fact, it provides one of the most important proof rules in discrete mathematics...

> Well ordering commonly comes up in computer science as a method for proving
that computations won’t run forever. The idea is to assign a value to each
successive step of a computation so that the values get smaller at every step.
If the values are all from a well ordered set, then the computation can’t run
forever, because if it did, the values assigned to its successive steps would
define a subset with no minimum element. You’ll see several examples of this
technique applied in Chapter 6 to prove that various state machines will
eventually terminate.

Given we understand the definitions of **well-ordered** and **Well Ordering
Principle** we only need to prove what is left as the exercise in the textbook
(Problem 2.20):

> Now it is easy to verify that 𝑛<sub>𝑠</sub> + 𝑓<sub>𝑠</sub> is the minimum
element of S (Problem 2.20).

To prove this statement, let's assume the opposite:

There are
<span class="math-inline">𝑛<sub>𝑠'</sub></span>
and
<span class="math-inline">𝑓<sub>𝑠'</sub></span>
so that
<span class="math-inline">𝑛<sub>𝑠'</sub> + 𝑓<sub>𝑠'</sub></span> is the minimum
element of 𝑆, which means that

<div class="math-block">𝑛<sub>𝑠'</sub> + 𝑓<sub>𝑠'</sub> < 𝑛<sub>𝑠</sub> + 𝑓<sub>𝑠</sub>&nbsp;&nbsp;&nbsp;(1A)</div>

Let's consider two cases:

1) <b>𝑛<sub>𝑠'</sub> = 𝑛<sub>𝑠</sub></b>, which reduces the equation 1A to just:

<div class="math-block">𝑓<sub>𝑠'</sub> < 𝑓<sub>𝑠</sub>
</div>

which is a contradiction to the definition of
<span class="math-inline">𝑓<sub>𝑠</sub></span>
which is the smallest element of

<span class="math-inline">{ 𝑓 ∈ 𝔽 | 𝑛<sub>𝑠</sub> + 𝑓 ∈ S }</span>.

2) <b>𝑛<sub>𝑠'</sub> ≠ 𝑛<sub>𝑠</sub></b>

Let's group members of the equation 1A:
<span class="math-inline">𝑛<sub>𝑠</sub></span>
with
<span class="math-inline">𝑛<sub>𝑠'</sub></span>
to the left side of the equation and
<span class="math-inline">𝑓<sub>𝑠</sub></span>
with
<span class="math-inline">𝑓<sub>𝑠’</sub></span> to the right side:

<div class="math-block">𝑛<sub>𝑠’</sub> - 𝑛<sub>𝑠</sub> < 𝑓<sub>𝑠</sub> - 𝑓<sub>𝑠’</sub>&nbsp;&nbsp;&nbsp;(2A)
</div>

By definition of
<span class="math-inline">𝑛<sub>𝑠</sub></span>
, it is the smallest of
<span class="math-inline">{ 𝑛 ∈ ℕ | 𝑛 + 𝑓 ∈ S, for 𝑓 ∈ 𝔽 }</span>
which means that
<span class="math-inline">𝑛<sub>𝑠’</sub></span>
is greater than
<span class="math-inline">𝑛<sub>𝑠</sub></span>
i.e.
<span class="math-inline">𝑛<sub>𝑠'</sub> - 𝑛<sub>𝑠</sub> ≥ 1</span>

Let's obtain the contradiction by proving that the right side of the equation 2A
is always less than 1:

<span class="math-inline">𝑓<sub>𝑠</sub> ∈ 𝔽</span>
and
<span class="math-inline">𝑓<sub>𝑠'</sub> ∈ 𝔽</span>
so by definition of
<span class="math-inline">𝔽</span>:

<div class="math-block">𝑠 / (𝑠 + 1) - 𝑠' / (𝑠' + 1) < 1, where 𝑠 ∈ ℕ and 𝑠' ∈ ℕ
</div>

Let's multiply both parts by
<span class="math-inline">(𝑠 + 1) × (𝑠' + 1)</span>
to get rid of the fractions:

<div class="math-block">𝑠 × (𝑠' + 1) - 𝑠' × (𝑠 + 1) < (𝑠 + 1) × (𝑠' + 1)
𝑠 × 𝑠' + 𝑠 - 𝑠' × 𝑠 - 𝑠' < 𝑠 × 𝑠' + 𝑠 + 𝑠' + 1
</div>

Reduction gives us:

<div class="math-block">-𝑠' × 𝑠 - 𝑠' < 𝑠' + 1
-𝑠' × 𝑠 - 2 × 𝑠' < 1
𝑠' × (𝑠 + 2) > -1
</div>

This equation always holds since both
<span class="math-inline">𝑠</span>
and
<span class="math-inline">𝑠'</span>
are nonnegative integers, which
proves that the right side of the equation 1A is always less than 1.

At the same time we have showed already that the left side of the equation 1A
is greater or equal to 1 which means that we arrived to the contradiction in the
equation 1A.

We have just proved the homework exercise `Problem 2.20`, the final building
block for proof of Lemma 2.4.6.

<a name="proof-2" href="#proof-2"></a>

### 2. Proof that `𝑣` is a strictly decreasing derived variable

Let's actually check the following statement:

> Now it’s easy to check that if `(𝑥, 𝑦) → (𝑥', 𝑦')` is a legitimate robot
move, then `𝑣((𝑥', 𝑦')) < 𝑣((𝑥, 𝑦))`. In particular, v is a strictly decreasing
derived variable...

We need to check if `𝑣((𝑥', 𝑦')) < 𝑣((𝑥, 𝑦))` holds for both types of moves
that a robot can do:

1) **a unit distance West move** — that is, `(𝑥, 𝑦) → (x − 1, 𝑦)` for `x > 0`

By definition `𝑣(𝑥, 𝑦) := 𝑦 + 𝑥 / (𝑥 + 1)`, so for `(𝑥, 𝑦)` and `(𝑥', 𝑦')`
coordinates we have:

<div class="math-block">𝑣((𝑥, 𝑦)) > 𝑣((𝑥', 𝑦'))</div>

Expand by definition of
<span class="math-inline">𝑣</span>
:

<div class="math-block">𝑦 + 𝑥 / (𝑥 + 1) > 𝑦' + 𝑥' / (𝑥' + 1)</div>

Replace
<span class="math-inline">𝑥'</span>
with
<span class="math-inline">(𝑥 - 1)</span>
,
<span class="math-inline">𝑦'</span>
with
<span class="math-inline">𝑦</span>
:

<div class="math-block">𝑦 + 𝑥 / (𝑥 + 1) > 𝑦 + (𝑥 - 1) / ((𝑥 - 1) + 1)</div>

Reduce
<span class="math-inline">𝑦</span>
and
<span class="math-inline">1</span>'s:

<div class="math-block">𝑥 / (𝑥 + 1) > (𝑥 - 1) / 𝑥</div>

Multiply both parts by
<span class="math-inline">𝑥 × (𝑥 + 1)</span>
to get rid of fractions

<div class="math-block">𝑥<sup>2</sup> > (𝑥 - 1)(𝑥 + 1)</div>

This equation always holds, so
<span class="math-inline">𝑣((𝑥, 𝑦)) > 𝑣((𝑥', 𝑦'))</span>
holds:

<div class="math-block">𝑥<sup>2</sup> > (𝑥<sup>2</sup> - 1)</div>

2) **a unit distance South combined with an arbitrary jump** East—that is,
`(𝑥, 𝑦) → (𝑧, 𝑦 − 1)` for `𝑧 ≥ 𝑥`.

<div class="math-block">𝑣((𝑥, 𝑦)) > 𝑣((𝑥', 𝑦'))</div>

Expand by definition of
<span class="math-inline">`𝑣`</span>
:

<div class="math-block">𝑦 + 𝑥 / (𝑥 + 1) > 𝑦' + 𝑥' / (𝑥' + 1)</div>

Replace
<span class="math-inline">𝑥'</span>
with
<span class="math-inline">𝑧</span>
,
<span class="math-inline">𝑦'</span>
with
<span class="math-inline">𝑦 - 1</span>
:

<div class="math-block">𝑦 + 𝑥 / (𝑥 + 1) > 𝑦 - 1 + 𝑧 / (𝑧 + 1)</div>

Reduce y:

<div class="math-block">𝑥 / (𝑥 + 1) > -1 + 𝑧 / (𝑧 + 1)</div>

Due to
<span class="math-inline">(𝑥 / 𝑥 + 1) < 1</span>
for any
<span class="math-inline">𝑥 ≥ 0</span>
and
<span class="math-inline">(𝑧 / 𝑧 + 1) < 1</span>
for any
<span class="math-inline">𝑧 ≥ 𝑥</span>
we have that
<span class="math-inline">𝑥 / (𝑥 + 1) - 𝑧 / (𝑧 + 1)</span>
is always greater than -1

So
<span class="math-inline">𝑣((𝑥, 𝑦)) > 𝑣((𝑥', 𝑦'))</span>
holds:

<div class="math-block">𝑥 / (𝑥 + 1) - 𝑧 / (𝑧 + 1) > -1</div>

<a name="proof-3" href="#proof-3"></a>

### 3. Implication of Theorem 6.3.3: Robot always gets stuck.

<img src="/images/2018-01-24-southeast-jumping-robot/Theorem-6.3.3.png"/>

This last section concludes the proof: in the step 2 we showed that a derived
variable
<span class="math-inline">𝑣</span>
is a strictly decreasing derived variable whose range is a well ordered set
<span class="math-inline">ℕ + 𝔽</span> so we conclude that for any sequence of
steps that robot can do it will eventually end up being in (0, 0).

<a name="geometric-interpretation"></a>

## Geometric interpretation

Let's consider that the robot is moving on 10 x 10 quadrant. By definition of
<span class="math-inline">𝑣</span> we have:

<div class="math-block">𝑣(𝑥, 𝑦) := 𝑦 + 𝑥 / (𝑥 + 1)</div>
therefore we get the
following table of values:

    (9 + 0/1)    (9 + 1/2)    (9 + 2/3)   ... (9 + 9/10)  # 9 ≤ y + x / (x + 1) ≤ 10
    ...                     ...                      ...
    (2 + 0/1)    (2 + 1/2)    (2 + 2/3)   ... (2 + 9/10)  # 2 ≤ y + x / (x + 1) ≤ 3
    (1 + 0/1)    (1 + 1/2)    (1 + 2/3)   ... (1 + 9/10)  # 1 ≤ y + x / (x + 1) ≤ 2
    (0 + 0/1)    (0 + 1/2)    (0 + 2/3)   ... (0 + 9/10)  # 0 ≤ y + x / (x + 1) ≤ 1

We see that the rows form buckets of values constrained within the range of [𝑦, 𝑦 + 1], for
each { 𝑦 ∈ ℕ | 0 ≤ 𝑦 ≤ 10 }:

<div class="math-block">𝑦 ≤ 𝑦 + 𝑥 / (𝑥 + 1) < 𝑦 + 1   (Observation 1)
</div>

for example
<span class="math-inline">2 ≤ (2 + 0/1) < (2 + 1/2) < (2 + 2/3) < ... < (2 + 9/10) < 3</span>.

Also, we see that columns form buckets of points so that the difference between
the values of any two adjacent points equals to 1, for example:

<div class="math-block">(2 + 2/3) - (1 + 2/3) = 1  (Observation 2)</div>

**Observation 3. Sequences from the vertical buckets decrease
with a rate of 1 per row and the sequences from the horizontal buckets decrease
with a rate strictly less than 1 per column so vertical sequences decrease faster**.

When robot jumps to the West it changes the column bucket which means that
the
<span class="math-inline">𝑦</span>
stays the same, but
<span class="math-inline">𝑥</span> changes to
<span class="math-inline">𝑥 - 1</span>
, for example:

<div class="math-block">(5, 5, 5 + 5/6) ⟶ (4, 5, 5 + 4/5)  # 5 + 5 / 6 > 5 + 4/5
</div>

When robot jumps to the South East it changes the column and row buckets which
means that

<div class="math-block">(5, 5, 5 + 5/6) ⟶ (𝑘, 4, 4 + (𝑘) / (𝑘 + 1)), 5 ≤ k ≤ 10
</div>

Along 𝑥-axis, Robot can jump to a 𝑘 coordinate as far as the right boundary of a quadrant, however its jump also changes the horizontal bucket
<span class="math-inline">𝑦 - 1</span>
which means that this jump to South is always a stronger contributor to the
value 𝑣 than an arbitrary jump to the East (this is obvious from the
observations 1, 2 and 3).

Now is clear that after each of these two moves derived value
<span class="math-inline">𝑣</span>
becomes smaller than (5, 5).

### Plots

Let's look at the geometric interpretation of this function:

<div class="math-block">𝑓(𝑥, 𝑦) = 𝑦 + 𝑥 / (𝑥 + 1)
</div>

This is a three-dimensional function
<span class="math-inline">𝑧 = 𝑦 + 𝑥 / (𝑥 + 1)</span>
so we will need a 3D plot to visualize this function:

<img src="/images/2018-01-24-southeast-jumping-robot/Academo-Annotated.jpg"/>

Let's assume that the robot is jumping from (5, 5) coordinate to either
(4, 5) with its "unit distance West move" or (8, 4) with its "unit distance
South combined with an arbitrary jump".

When I look at the annotated plot above, I see a good analogy: the plot
represents a fragment of a mountain which the robot is trying climb up: values
of
<span class="math-inline">𝑧</span>
like (5 + 5/6) or (4 + 8/9) represent the altitudes corresponding to the
coordinates
<span class="math-inline">(𝑥, 𝑦)</span> of robot's positions.

The drama of this robot, however, is that it can only move down the hill so it
can never climb up. The altitude of its position is always decreasing and since
it jumps on a limited 10 x 10 quadrant and the points are nonnegative integer
numbers, the termination claim that we proved asserts that sooner or later robot
will reach coordinate (0, 0) and get stuck.

The following plots demonstrate how the function
<span class="math-inline">𝑓(𝑥, 𝑦) = 𝑦 + 𝑥 / (𝑥 + 1)</span> looks like when it is
not discrete but more continuous. These plots demonstrate it even better that
the function is decreasing to 0 both along
<span class="math-inline">𝑥</span>
and
<span class="math-inline">𝑦</span>
axes.

<details>
<summary>3D Plot by Wolfram</summary>
<img src="/images/2018-01-24-southeast-jumping-robot/Wolfram.jpg"/>
</details>

<details>
<summary>3D Plot by Academo (Front)</summary>
<img src="/images/2018-01-24-southeast-jumping-robot/AcademoFront.jpg"/>
</details>

<details>
<summary>3D Plot by Academo (Back)</summary>
<img src="/images/2018-01-24-southeast-jumping-robot/AcademoBack.jpg"/>
</details>

<a name="credits"></a>

## Credits

I am working with this proof because it is the material for the Week 2 of the
course: "Formal Software Verification" [[2]](#anchor_02_course). It is unlikely
that I would have encountered this problem otherwise.

I used to two online services: Wolfram|Alpha [[3]](#anchor_03_wolframalpha) and
Academo.org [[4]](#anchor_04_academo) to draw the plots. I used the amazing
Academo service to create the annotated plot which helped me to visualize and
understand the geometric interpretation of the proof.

<a name="links"></a>

## Links

<a name="anchor_01_mathematics"></a>
[1] [Eric Lehman, F Thomson Leighton, Albert R Meyer, "Mathematics for Computer
Science", revised Monday 5th June, 2017, 19:42.](https://courses.csail.mit.edu/6.042/spring17/mcs.pdf)

<a name="anchor_02_course"></a>
[2] [edx - Formal Software Verification](https://www.edx.org/course/formal-software-verification-usmx-umuc-stv1-3x)

<a name="anchor_03_wolframalpha"></a>
[3] <a href="http://www.wolframalpha.com/input/?i=plot">Wolfram\|Alpha</a>

<a name="anchor_04_academo"></a>
[4] <a href="https://academo.org/demos/3d-surface-plotter/?expression=y%2Bx%2F(x%2B1)&xRange=0%2C+10&yRange=0%2C+10&resolution=100">Academo</a>
