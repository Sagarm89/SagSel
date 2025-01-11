# frozen_string_literal: true

# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

require File.expand_path('../spec_helper', __dir__)
require File.expand_path('../../../../../lib/selenium/webdriver/bidi/network/set_cookie_headers', __dir__)

module Selenium
  module WebDriver
    class BiDi
      describe SetCookieHeaders do
        let(:set_cookie_headers) { described_class.new }

        describe '#initialize' do
          it 'initializes with an empty hash by default' do
            expect(set_cookie_headers.all).to eq({})
          end

          it 'stores the passed set_cookie_headers hash internally' do
            my_hash = {'first_cookie' => {value: 'abc123'}}
            cookie_headers = described_class.new(my_hash)
            expect(cookie_headers.all).to eq(my_hash)
          end
        end

        describe '#all' do
          it 'returns the entire internal set_cookie_headers hash' do
            set_cookie_headers['cookie1'] = 'value1'
            expect(set_cookie_headers.all).to eq({'cookie1' => {value: 'value1'}})
          end
        end

        describe '#add_set_cookie_header' do
          it 'adds a cookie header to the internal store with a default hash' do
            set_cookie_headers['name'] = 'chocolate_chip'
            expect(set_cookie_headers['name']).to eq({value: 'chocolate_chip'})
          end

          it 'overwrites an existing cookie header if the name already exists' do
            set_cookie_headers['cookie_name'] = 'old_value'
            set_cookie_headers['cookie_name'] = 'new_value'
            expect(set_cookie_headers['cookie_name']).to eq({value: 'new_value'})
          end
        end

        describe '#remove_set_cookie_header' do
          it 'removes the named cookie header' do
            set_cookie_headers['session_id'] = 'abc123'
            set_cookie_headers.delete('session_id')
            expect(set_cookie_headers['session_id']).to be_nil
          end

          it 'does not raise an error if the cookie header does not exist' do
            expect { set_cookie_headers.delete('non_existent') }.not_to raise_error
          end
        end

        describe '#[]=' do
          it 'adds or updates a cookie header via bracket assignment' do
            set_cookie_headers['key1'] = 'value1'
            expect(set_cookie_headers['key1']).to eq({value: 'value1'})

            set_cookie_headers['key1'] = 'updated_value'
            expect(set_cookie_headers['key1']).to eq({value: 'updated_value'})
          end
        end

        describe '#[]' do
          it 'retrieves the cookie header hash by name' do
            set_cookie_headers['key2'] = 'value2'
            expect(set_cookie_headers['key2']).to eq({value: 'value2'})
          end

          it 'returns nil if the cookie header does not exist' do
            expect(set_cookie_headers['does_not_exist']).to be_nil
          end
        end

        describe '#delete' do
          it 'removes a cookie header via bracket-based delete' do
            set_cookie_headers['key3'] = 'value3'
            set_cookie_headers.delete('key3')
            expect(set_cookie_headers['key3']).to be_nil
          end
        end

        describe '#serialize' do
          context 'when set_cookie_headers is nil' do
            let(:initial_hash) { nil }

            it 'returns an empty array if no set_cookie_headers are provided' do
              expect(set_cookie_headers.serialize).to eq([])
            end
          end
        end
      end
    end
  end
end
