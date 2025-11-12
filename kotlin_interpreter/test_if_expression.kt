fun main() {
    // Test 1: Simple if expression
    val x = if (true) 10 else 20
    println(x)
    
    // Test 2: If expression with comparison
    val y = if (5 > 3) "yes" else "no"
    println(y)
    
    // Test 3: If expression with blocks
    val z = if (10 > 5) {
        val temp = 100
        temp + 50
    } else {
        val temp = 200
        temp + 100
    }
    println(z)
    
    // Test 4: Nested if expression
    val a = if (true) {
        if (false) 1 else 2
    } else {
        3
    }
    println(a)
    
    println("All if expression tests passed!")
}
