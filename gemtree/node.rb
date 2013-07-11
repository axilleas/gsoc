#!/usr/bin/env ruby

require "net/http"
require "uri"
require "rubygems"
require "json"
require "pp"

class Node

  attr_accessor :package, :dependencies, :version, :parent

  def initialize (package, dependencies, version, parent)
    @package = package
    @dependencies = dependencies
    @version = version
    @parent = parent
  end


  def gem_dependencies

    uri = URI.parse("https://rubygems.org/api/v1/gems/#{@package}.json")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE

    request = Net::HTTP::Get.new(uri.request_uri)

    response = http.request(request)

    if response.code == "200"
    
      json = JSON.parse(response.body)   
      deps = json["dependencies"]
      runtime_deps = deps["runtime"]
    
      return runtime_deps
    
    else
    
      puts response.code
    
    end
    
  end

end
