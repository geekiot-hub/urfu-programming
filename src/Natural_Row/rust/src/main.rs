use num_bigint::BigUint;
use num_traits::cast::ToPrimitive;
use std::io;

fn main() {
    let mut string = String::new();

    println!("Enter power.");
    io::stdin()
        .read_line(&mut string)
        .expect("Lol, read line error.");

    let power: u32 = string.trim().parse().expect("Lol, power error.");

    println!("Calculating...");

    let mut n = BigUint::new(vec![10]).pow(power);

    let mut digits = BigUint::new(vec![1]);
    let mut count = BigUint::new(vec![9]);

    let one = BigUint::new(vec![1]);
    let nine = BigUint::new(vec![9]);
    let ten = BigUint::new(vec![10]);

    while n > &digits * &count {
        n -= &digits * &count;
        digits += &one;
        count *= &ten;
    }

    let number = (&count / &nine) + (&n - &one) / &digits;
    let index = ((n - one) % digits).to_usize().expect("Lol, usize error");

    let result = number
        .to_string()
        .chars()
        .nth(index)
        .expect("Lol, result error");

    println!("{}", result);
}
