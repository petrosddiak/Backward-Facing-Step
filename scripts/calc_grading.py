import sys

def f(R, L, n, h1):
    """
    OpenFOAM geometric grading formula:
    r = R^(1/(n-1))
    h1 = L * (1 - r) / (1 - r^n)
    We want to find R where f(R) = 0
    """
    if abs(R - 1.0) < 1e-7:
        return h1 * n - L
    try:
        r = R ** (1.0 / (n - 1))
        if abs(r - 1.0) < 1e-7:
            return h1 * n - L
        return h1 * (1 - r**n) / (1 - r) - L
    except (OverflowError, ZeroDivisionError):
        return float('inf')

def solve_expansion_ratio(L, n, h1):
    """Uses the Bisection method to find the correct R."""
    if abs(h1 - (L / n)) < 1e-6:
        return 1.0

    # Ensure h1 is mathematically possible
    if h1 >= L:
        print("Error: Desired cell height cannot be larger than the segment length.")
        sys.exit(1)

    low, high = 1.0, 1e9
    
    # Bisection algorithm
    for _ in range(100):
        mid = (low + high) / 2.0
        f_mid = f(mid, L, n, h1)
        f_low = f(low, L, n, h1)

        if f_mid == float('inf'):
            high = mid
            continue

        if f_mid * f_low < 0:
            high = mid
        else:
            low = mid

        if abs(high - low) < 1e-7:
            break

    return round(mid, 5)

def main():
    print("--- 2-Segment (50/50) Accurate Grading Calculator ---")
    try:
        total_L = float(input("Enter total edge length: "))
        total_n = int(input("Enter total cells along this edge: "))
        h1 = float(input("Enter desired first cell height: "))
    except ValueError:
        print("Invalid input.")
        return

    # 50% length, 50% cells
    seg1_L = total_L * 0.5
    seg1_n = total_n * 0.5
    seg1_n_int = round(seg1_n)

    if seg1_n_int <= 1:
        print("Error: Too few cells per segment. Increase cell count.")
        return

    # Calculate expansion ratio for the first half
    R_seg1 = solve_expansion_ratio(seg1_L, seg1_n_int, h1)
    
    # Inverse for the second half
    R_seg2 = round(1.0 / R_seg1, 5) if R_seg1 != 0 else 1.0

    print("\n====================================================")
    print("      Paste This into your Config File (`mesh_config.txt`)    ")
    print("====================================================")
    print(f"((0.5 0.5 {R_seg1})(0.5 0.5 {R_seg2}))")
    print("====================================================")

if __name__ == "__main__":
    main()