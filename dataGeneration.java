import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class dataGeneration {
	public static void main (String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader("goodata2"));
		String currentLine = br.readLine();
		String s = "";
		StringTokenizer st = new StringTokenizer(s);
		
		ArrayList<ArrayList<Double>> vectors = new ArrayList<ArrayList<Double>>();
		
		while (currentLine != null) {
			// System.out.println(currentLine);
			s += solve(currentLine);
			// System.out.println(solve(currentLine));
			
			st = new StringTokenizer(solve(currentLine));
			
			if (st.hasMoreTokens()) break;
			
			st.nextToken();
			
			ArrayList<Double> vector = new ArrayList<Double>();
			
			for (int i = 0; i < 35 && st.hasMoreTokens(); i++) {
				vector.add(Double.parseDouble(st.nextToken()));
			}
			
			if (vector.size() == 35) {
				vectors.add(vector);
			} else {
				// System.out.println( solve(currentLine) );
			}
			
			currentLine = br.readLine();
			
		}
		
		s = solve(s);		
		// System.out.println(vectors);
		
		int ct = 0;
		// System.out.println("finalizedData = []");
		
		for (ArrayList<Double> vector : vectors) {
			System.out.printf("goodPlankList%d = []\n", ct);
			for (int j = 0; j < 35; j++)
				System.out.printf("goodPlankList%d.append(%f)\n", ct, vector.get(j));
			System.out.printf("goodPlankList%d.append(%f)\n", ct, 1.0);
			System.out.printf("finalizedData.append(normalize(goodPlankList%d))\n", ct);
			ct++;
		}
		
		
		System.out.println("for dataPoint in finalizedData:");
		System.out.println("\tprint(dataPoint)");
		
		
	}
	
	static String solve(String s) {
		String r = "";
		
		for (int i = 0; i < s.length(); i++) {
			if (s.charAt(i) >= '0' && s.charAt(i) <= '9') {
				r += s.charAt(i);
			} else if (s.charAt(i) == ' ' || s.charAt(i) == '.') {
				r += s.charAt(i);
			}
		}
		
		return r;
	}
}
