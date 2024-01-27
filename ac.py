## An AC (arithmetic coding) implementation 
#  A.k.a. ACUC (under construction)
# See: https://en.wikipedia.org/wiki/Arithmetic_coding
#      https://link.springer.com/book/10.1007/978-1-4615-0799-4 (JPEG 2000)




''' 
A simple C# implementation of a binary arithmetic coder (BAC)
class aritmetic_coder
{
    List<decimal> fx, Fx;
    decimal  code = 0.0m, C = 0.0m, A = 1.0m;
    const double probability = 1.0 / 32.0;
    double[] symbol_freq = new double[2] {1.0 - probability, probability};

    /// ....
    public void encode()
    {
       foreach (char symbol in text)
       {
          int index = symbol_freq_map[symbol - '0'];
          C += Fx[index] * A;
          A *= fx[index];
       }
       if (A == 0m)
       {
          throw new Exception("Message too long!");
       }
       code = C + A / 2m;
    }
    /// ....
    public void decode()
    {
       int length = text.Length;
       text = "";
       for (int i = 0; i < length; ++i)
       {
          int index = extract(code);
          code -= Fx[index];
          code /= fx[index];  
                       
          int symbol = symbol_freq_unmap[index];
          text += Convert.ToChar(symbol + '0');
       }
    }    
}
'''