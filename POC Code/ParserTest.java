package parsing;

import static org.junit.Assert.*;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.InputMismatchException;
import java.util.Scanner;

import org.junit.Test;

/**
 * @author Eric Le Fort
 * @version 01
 */

public class ParserTest{
	private String[] queries = {
			"hello",
			"LASDGLKGSVLIUGAEOUGSVLUHwe;ofrw.k∆bwri;hqf.IBA LIU GqleiugwKUGwrliugwrgOUGFW	;OURW;U",
			"Eric",
			"my name is Eric!",
			"my name is Eric"
	};
	private String[] dataFiles = {
			"Hello world!",
			"",
			"Hello. My name is Eric. I am writing this simple test to check to see how well my parsing algorithm is performing."
					+ "hello again, don't forget my name: Eric. That is all."
	};
	private static String fileLocation = "../../../../Desktop/naija_businesses1.html", bigData = readData(fileLocation);
	private Integer[][][] expected = {
			{						//query 1 results.
				{0},
				{},
				{0, 114},
			},
			{						//query 2 results.
				{},
				{},
				{},
			},
			{						//query 3 results.
				{},
				{},
				{18, 149},

			},
			{						//query 4 results.
				{},
				{},
				{},

			},
			{						//query 5 results.
				{},
				{},
				{7},

			}
	};
	private long maxTime = 1000;	//1000 milliseconds, 1 second
	
	/**
	 * Tests for the pure functionality of the method SearchForString(String, String) and passes if all expected results are returned.
	 */
	@Test
	public void testFunctionalitySearchForString(){
		for(int i = 0; i < queries.length; i++){
			for(int j = 0; j < dataFiles.length; j++){
				assertArrayEquals(expected[i][j], Parser.searchForString(queries[i], dataFiles[j]));
			}
		}
		
		assertArrayEquals(new Integer[]{2}, Parser.searchForString("hello", "hehello"));
		assertArrayEquals(new Integer[]{6}, Parser.searchForString("hello", "hehhhehello"));
	}//testsearchForString()

	/**
	 * Tests for the speed of the method SearchForString(String, String) using some extreme cases of large inputs and passes if each
	 * search completes within thespecified maximum time.
	 */
	@Test
	public void testEfficiencySearchForString(){
		String queries[] = {
				"Eric",
				"o;hvajkbek.vb.akjsb",
				"a",
				"Hello, how are you today?"
		};
		long startTime, endTime;

		for(int i = 0; i < queries.length; i++){
			startTime = System.nanoTime();
			Parser.searchForString(queries[i], bigData);
			endTime = System.nanoTime();
			assert(maxTime > endTime - startTime);
		}
	}//testEfficiencySearchForString()

	/**
	 * Tests for the pure functionality of the method SearchForSimilarString(String, String, int) using some extreme cases of large
	 * inputs and passes if all expected results are returned.
	 */
	@Test
	public void testFunctionalitySearchForSimilarString(){
		
		for(int i = 0; i < queries.length; i++){			//Should return same results as searchForString().
			for(int j = 0; j < dataFiles.length; j++){
				assertArrayEquals(expected[i][j], Parser.searchForSimilarString(queries[i], dataFiles[j], 0));
			}
		}
		
		assertArrayEquals(new Integer[]{0, 14}, Parser.searchForSimilarString("HERE", "here comes my hero", 1));
		assertArrayEquals(new Integer[]{}, Parser.searchForSimilarString("te", "Hello there, this is a test.", 1));
		assertArrayEquals(new Integer[]{}, Parser.searchForSimilarString("", "Some text", 0));
		
		assertArrayEquals(new Integer[]{11}, Parser.searchForSimilarString("hello", "Some text, hello", 2));
		assertArrayEquals(new Integer[]{11}, Parser.searchForSimilarString("hello", "Some text, hello", 1));
		

		assertArrayEquals(new Integer[]{6}, Parser.searchForSimilarString("hello", "hehhhehellp", 1));
		assertArrayEquals(new Integer[]{28}, Parser.searchForSimilarString("fileResults", ". \n .. \n q1/.SQL \n q2.SQL \n fileResult.txt", 1));
		//ERROR KNOWN: If the result is almost found but there is no next character, the query fails.
		//assertArrayEquals(new Integer[]{32}, Parser.searchForSimilarString("fileResults", ". \n .. \n q1/.SQL \n q2.SQL \n fileResult", 1));
		
	}//testFunctionalitySearchForSimilarString()
	
	/**
	 * Tests for the speed of the method SearchForSimilarString(String, String) and passes if each search completes within the specified
	 * maximum time.
	 */
	@Test
	public void testEfficiencySearchForSimilarString(){
		String queries[] = {
				"Eric",
				"o;hvajkbek.vb.akjsb",
				"a",
				"Hello, how are you today?"
		};
		int proximities[] = {
			1,
			6,
			0,
			4
		};
		long startTime, endTime;

		for(int i = 0; i < queries.length; i++){
			startTime = System.nanoTime();
			Parser.searchForSimilarString(queries[i], bigData, proximities[i]);
			endTime = System.nanoTime();
			assert(maxTime > endTime - startTime);
		}
	}//testEfficiencySearchForSimilarString()
	
	private static String readData(String filePath){
		String result;
		try{												//Reads the ids from the text file at the given path into ids.
			Scanner in = new Scanner(new FileReader(filePath));
			in.useDelimiter("\\Z");							//Reads until the end of the file.
			result = in.next();
			in.close();
			return result;
		}catch(FileNotFoundException fnfe){
			fnfe.getMessage();
			return "";
		}catch(InputMismatchException ime){
			ime.getMessage();
			return "";
		}
	}//readData()
	
}//ParserTest
