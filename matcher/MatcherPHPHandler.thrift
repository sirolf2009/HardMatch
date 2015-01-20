namespace java com.hardmatch.matcher.thrift

struct Store {
1: string name
2: double price
}

service MatcherPHPHandler {

  /**
   * Match the specified components to the cheapest store
   * @param components - a list of components to be matched
   * @return a map with components name as key and the according store as value
   */
   map<string, Store> match(1: list<string> components)

}