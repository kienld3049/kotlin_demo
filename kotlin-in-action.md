



(⁨24⁩ of ⁨559⁩)



CONTENTSxiv
12.2 Reflection: Introspecting Kotlin objects at run time 342
The Kotlin reflection API: KClass, KCallable, KFunction, and
KProperty 343 ■ Implementing object serialization using
reflection 347 ■ Customizing serialization with annotations 348
JSON parsing and object deserialization 352 ■ The final step of
deserialization: callBy() and creating objects using reflection 356
13 DSL construction 361
13.1 From APIs to DSLs: Creating expressive custom
code structures 362
Domain-specific languages 363 ■ Internal DSLs are seamlessly
integrated into the rest of your program 364 ■ The structure of
DSLs 365 ■ Building HTML with an internal DSL 366
13.2 Building structured APIs: Lambdas with receivers
in DSLs 368
Lambdas with receivers and extension function types 368 ■ Using
lambdas with receivers in HTML builders 372 ■ Kotlin builders:
Enabling abstraction and reuse 377
13.3 More flexible block nesting with the
invoke convention 380
The invoke convention: Objects callable as functions 380 ■ The
invoke convention in DSLs: Declaring dependencies in Gradle 381
13.4 Kotlin DSLs in practice 383
Chaining infix calls: The should function in test frameworks 383
Defining extensions on primitive types: Handling dates 384
Member extension functions: Internal DSL for SQL 385
P ART 3 CONCURRENT PROGRAMMING WITH COROUTINES
AND FLOWS ........................................................391
14 Coroutines 393
14.1 Concurrency vs. parallelism 394
14.2 Concurrency the Kotlin way: Suspending functions
and coroutines 394
14.3 Comparing threads and coroutines 395
14.4 Functions that can pause: Suspending functions 397
Code written with suspending functions looks sequential 398
14.5 Comparing coroutines to other approaches 400
Calling a suspending function 401
CONTENTS xv
14.6 Entering the world of coroutines: Coroutine builders 402
From regular code into the realm of coroutines: The runBlocking
function 403 ■ Creating start-and-forget coroutines: The launch
function 404 ■ Awaitable computations: The async builder 407
14.7 Deciding where your code should run: Dispatchers 409
Choosing a dispatcher 409 ■ Passing a dispatcher to a coroutine
builder 412 ■ Using withContext to switch the dispatcher within a
coroutine 412 ■ Coroutines and dispatchers aren’t a magical fix
for thread-safety concerns 413
14.8 Coroutines carry additional information in their
coroutine context 415
15 Structured concurrency 418
15.1 Coroutine scopes establish structure between coroutines 419
Creating a coroutine scope: The coroutineScope function 420
Associating coroutine scopes with components: CoroutineScope 421
The danger of GlobalScope 423 ■ Coroutine contexts and
structured concurrency 425
15.2 Cancellation 427
Triggering cancellation 428 ■ Invoking cancellation automatically
after a time limit has been exceeded 429 ■ Cancellation cascades
through all children 430 ■ Cancelled coroutines throw
CancellationExceptions in special places 431 ■ Cancellation
is cooperative 432 ■ Checking whether a coroutine has been
cancelled 433 ■ Letting other coroutines play: The yield
function 434 ■ Keep cancellation in mind when acquiring
resources 436 ■ Frameworks can perform cancellation for you 437
16 Flows 441
16.1 Flows model sequential streams of values 441
Flows allow you to work with elements as they are emitted 442
Different types of flows in Kotlin 443
16.2 Cold flows 444
Creating a cold flow with the flow builder function 444 ■ Cold
flows don’t do any work until collected 445 ■ Cancelling the
collection of a flow 447 ■ Cold flows under the hood 448
Concurrent flows with channel flows 449
16.3 Hot flows 452
Shared flows broadcast values to subscribers 453 ■ Keeping track of
state in your system: State flow 458 ■ Comparing state flows and shared
flows 462 ■ Hot, cold, shared, state: When to use which flow 464
CONTENTSxvi
17 Flow operators 466
17.1 Manipulating flows with flow operators 466
17.2 Intermediate operators are applied to an upstream flow
and return a downstream flow 467
Emitting arbitrary values for each upstream element: The transform
function 468 ■ The take operator family can cancel a flow 469
Hooking into flow phases with onStart, onEach, onCompletion, and
onEmpty 469 ■ Buffering elements for downstream operators and
collectors: The buffer operator 471 ■ Throwing away intermediate
values: The conflate operator 474 ■ Filtering out values on a
timeout: The debounce operator 475 ■ Switching the coroutine
context on which a flow is executed: The flowOn operator 476
17.3 Creating custom intermediate operators 477
17.4 Terminal operators execute the upstream flow and may
compute a value 478
Frameworks provide custom operators 478
18 Error handling and testing 480
18.1 Handling errors thrown inside coroutines 481
18.2 Error propagation in Kotlin coroutines 483
Coroutines cancel all their children when one child fails 483
Structured concurrency only affects exceptions thrown across
coroutine boundaries 485 ■ Supervisors prevent parents
and siblings from being cancelled 486
18.3 CoroutineExceptionHandler: The last resort
for processing exceptions 488
Differences when using CoroutineExceptionHandler with launch
or async 491
18.4 Handling errors in flows 493
Processing upstream exceptions with the catch operator 494 ■ Retry
the collection of a flow if predicate is true: The retry operator 495
18.5 Testing coroutines and flows 496
Making tests using coroutines fast: Virtual time and the test
dispatcher 497 ■ Testing flows with Turbine 500
appendix A Building Kotlin projects 503
appendix B Documenting Kotlin code 507
appendix C The Kotlin ecosystem 511
index 515
xvii
preface
The idea for Kotlin was conceived at JetBrains in 2010. By that time, JetBrains was an
established vendor of development tools for many languages, including Java, C#,
JavaScript, Python, Ruby, and PHP. IntelliJ IDEA, the Java IDE that is our flagship
product, also included plugins for Groovy and Scala.
The experience of building the tooling for such a diverse set of languages gave us a
unique understanding of and perspective on the language design space as a whole.
And yet the IntelliJ Platform-based IDEs, including IntelliJ IDEA, were still being
developed in Java.
We were somewhat envious of our colleagues on the .NET team who were develop-
ing in C#, a modern, powerful, and rapidly evolving language. But we didn’t see any lan-
guage we could use in place of Java. What were our requirements for such a language?
The first and most obvious requirement was static typing. We don’t know any other
way to develop a multimillion-line codebase over many years without going crazy. Sec-
ond, we needed full compatibility with the existing Java code. That codebase is a
hugely valuable asset for JetBrains, and we couldn’t afford to lose it or devalue it
through difficulties with interoperability. Third, we didn’t want to accept any compro-
mises in terms of tooling quality. Developer productivity is the most important value to
JetBrains, and great tooling is essential to achieving that. Finally, we needed a lan-
guage that was easy to learn and reason about.
When we see an unmet need for our company, we know there are other companies
in similar situations, and we expect our solution to find many users outside of Jet-
Brains. With this in mind, we decided to embark on the project of creating a new lan-
guage: Kotlin.
PREFACExviii
As it happens, the project took longer than we expected, and Kotlin 1.0 came out
more than five years after the first commit to the repository. Since then, the language
has found its audience, grown into a wonderful ecosystem of its own, and is here to stay.
Kotlin is named after an island near St. Petersburg, Russia. In using the name of an
island, we followed the precedent established by Java and Ceylon. (In English, the
name is usually pronounced “cot-lin,” not “coat-lin” or “caught-lin.”)
As the language was approaching release, we realized it would be valuable to have
a book about Kotlin, written by people who were involved in making design decisions
for the language and who could confidently explain why things are the way they are in
Kotlin. This book is a result of that effort, and we hope it will help you learn and under-
stand the Kotlin language. Good luck, and may you always develop with pleasure!
xix
acknowledgments
First of all, we’d like to thank Sergey Dmitriev and Max Shafirov for believing in the
idea of a new language and deciding to invest JetBrains’ resources. Without them, nei-
ther the language nor this book would exist.
We would especially like to acknowledge Andrey Breslav, who is the main person to
blame for designing a language that’s a pleasure to write about (and to code in). Andrey,
despite having to lead the continuously growing Kotlin team, was able to give us a lot of
helpful feedback for the first edition of this book, which we greatly appreciate.
We’re grateful to the team at Manning, who guided us through the process of writ-
ing this book and helped make the text readable and well structured—particularly
our development editors, Dan Maharry and Marina Michaels, who bravely strove to
find time to talk despite our busy schedules, as well as Michael Stephens, Helen Ster-
gius, Kevin Sullivan, Tiffany Taylor, Elizabeth Martin, and Marija Tudor. In addition,
we thank the rest of the production staff who helped format this book.
The feedback from our technical reviewers, Igor Wojda and Brent Watson, was also
invaluable, as were the comments of the reviewers who read the manuscript during
the development process: Robert Wenner, Alessandro Campeis, Amit Lamba, Angelo
Costa, Boris Vasile, Brendan Grainger, Calvin Fernandes, Christopher Bailey, Christo-
pher Bortz, Conor Redmond, Dylan Scott, Filip Pravica, Jason Lee, Justin Lee, Kevin
Orr, Nicolas Frankel, Paweł Gajda, Ronald Tischliar, and Tim Lavers.
Thanks also go to everyone who submitted feedback during the MEAP program
and in the book’s forum; we’ve improved the text based on your comments: Alessan-
dro Campeis, Bob Resendes, Didier Garcia, Haim Raman, James Watson, João Miguel
ACKNOWLEDGMENTSxx
Pires Dias, Jorge Ezequiel Bo, Mark Kotyk, Md Shahriar Anwar, Mikael Dautrey, Nitin
Gode, Peter Szabo, Phillip Sorensen, Rani Sharim, Richard Meinsen, Sergio Britos,
Simeon Leyzerzon, Steve Prior, Walter Alexander Mata López, and William Morgan.
We’re grateful to the entire Kotlin team, who had to listen to frequent reports like,
“One more section is finished!” throughout the time we spent writing this book. We
want to thank our colleagues who helped us plan the book and gave feedback on its
drafts, especially Ilya Ryzhenkov, Michael Glukhikh, Ilya Gorbunov, Vsevolod Tolstopy-
atov, Dmitry Khalanskiy, and Hadi Hariri. We’d also like to thank our friends who not
only were supportive but also had to read the text and provide feedback (sometimes
in ski resorts during vacations): Lev Serebryakov, Pavel Nikolaev, Alex Semin, and
Alisa Afonina.
Finally, we’d like to thank our families and cats for making this world a better
place.
xxi
about this book
The second edition of Kotlin in Action teaches you the Kotlin programming language
and how to use it to build applications running on the Java virtual machine (JVM) and
Android. It starts with the basic features of the language and proceeds to cover the
more distinctive aspects of Kotlin, such as its support for building high-level abstrac-
tions and domain-specific languages. The book also provides the information you
need to integrate Kotlin with existing Java projects and helps you introduce Kotlin
into your current working environment.
The book covers Kotlin 2.0. For ongoing updates about the new features and
changes, please refer to the online documentation at https://kotlinlang.org.
Who should read this book
Kotlin in Action, Second Edition, is primarily focused on developers with some level of
Java experience. Kotlin builds on many concepts and techniques from Java, and the
book strives to get you up to speed quickly by using your existing knowledge.
If you’re experienced with other programming languages such as C# or JavaScript,
you may need to refer to other sources of information to understand the more intri-
cate aspects of Kotlin’s interaction with the JVM, but you’ll still be able to learn Kotlin
using this book. We focus on the Kotlin language as a whole and not on a specific
problem domain, so the book should be equally useful for server-side developers,
Android developers, and everyone else who builds projects targeting the JVM.
ABOUT THIS BOOKxxii
How this book is organized: A road map
The book is divided into three parts. Part 1 explains how to get started using Kotlin
together with existing libraries and APIs:
■ Chapter 1 talks about the key goals, values, and areas of application for Kotlin,
and it shows you the different ways to run Kotlin code.
■ Chapter 2 explains the essential elements of any Kotlin program, including con-
trol structures and variable and function declarations.
■ Chapter 3 goes into detail about how functions are declared in Kotlin and intro-
duces the concept of extension functions and properties.
■ Chapter 4 is focused on class declarations and introduces the concepts of data
classes and companion objects.
■ Chapter 5 introduces the use of lambdas in Kotlin and showcases a number of
Kotlin standard library functions using lambdas.
■ Chapter 6 gives an overview of how you work with collections in Kotlin as well as
their lazy counterpart: sequences.
■ Chapter 7 familiarizes you with the concept of nullability.
■ Chapter 8 describes the Kotlin type system, including an additional focus on
collections.
Part 2 teaches you how to build your own APIs and abstractions in Kotlin and covers
some of the language’s deeper features:
■ Chapter 9 talks about the principle of conventions, which assigns special mean-
ing to methods and properties with specific names, and it introduces the con-
cept of delegated properties.
■ Chapter 10 shows how to declare higher-order functions—functions that take
other functions and parameters or return them. It also introduces the concept
of inline functions.
■ Chapter 11 is a deep dive into the topic of generics in Kotlin, starting with the
basic syntax and going into more advanced areas, such as reified type parame-
ters and variance.
■ Chapter 12 covers the use of annotations and reflection and is centered around
JKid, a small, real-life JSON serialization library that makes heavy use of those
concepts.
■ Chapter 13 introduces the concept of domain-specific languages, describes
Kotlin’s tools for building them, and demonstrates many DSL examples.
Part 3 covers coroutines and flows, the approach to performing concurrent program-
ming in Kotlin:
■ Chapter 14 provides an overview of Kotlin’s concurrency model, including sus-
pending functions, coroutines, and the basic mechanics of writing concurrent
code.
ABOUT THIS BOOK xxiii
■ Chapter 15 talks about the concept of structured concurrency, which helps you
manage concurrent tasks and introduces the mechanisms required for cancella-
tion and error handling.
■ Chapter 16 introduces flows, the coroutine-based abstraction used for model-
ing sequential streams of values over time.
■ Chapter 17 covers flow operators, which can be used to transform Kotlin flows,
in more detail.
■ Chapter 18 dives deeper into the subject of error handling and testing your
concurrent code.
The book also features three appendixes:
■ Appendix A explains how to build Kotlin code with Gradle and Maven.
■ Appendix B focuses on writing documentation comments and generating API
documentation for Kotlin modules.
■ Appendix C is a guide for exploring the Kotlin ecosystem and finding the latest
online information.
The book works best when you read it all the way through, but you’re also welcome to
refer to individual chapters covering specific subjects you’re interested in and to fol-
low the cross-references if you run into an unfamiliar concept.
About the code
The following typographical conventions are used throughout this book:
■ Italic font is used to introduce new terms.
■ Fixed-width font is used to denote code samples, as well as function names,
classes, and other identifiers.
Code annotations accompany many of the code listings and highlight important con-
cepts. Where necessary, the original source code has been reformatted; we’ve added
line breaks and reworked indentation to accommodate the available page space in the
book. In rare cases, even this was not enough, and listings include line-continuation
markers (➥).
Many source listings in the book show code together with its output. In those cases,
we show the output of the code as a line comment following the line that produces
the output or below the snippet, like this:
fun main() {
println("Hello World")
// Hello World
}
Some of the examples are intended to be complete runnable programs, whereas oth-
ers are snippets used to demonstrate certain concepts and may contain omissions
(indicated with ...) or syntax errors (described in the book text or in the examples
