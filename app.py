import streamlit as st
import requests
import pandas as pd

def get_candidate_bio(candidate_id, detailed=False):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    if detailed:
        url = f"http://api.votesmart.org/CandidateBio.getDetailedBio?key={api_key}&candidateId={candidate_id}&o=JSON"
    else:
        url = f"http://api.votesmart.org/CandidateBio.getBio?key={api_key}&candidateId={candidate_id}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error accessing the API: {response.status_code}"

def get_campaign_address(candidate_id):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Address.getCampaign?key={api_key}&candidateId={candidate_id}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error accessing the API: {response.status_code}"

def get_campaign_web_address(candidate_id):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Address.getCampaignWebAddress?key={api_key}&candidateId={candidate_id}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error accessing the API: {response.status_code}"

def get_office_address(candidate_id):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Address.getOffice?key={api_key}&candidateId={candidate_id}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error accessing the API: {response.status_code}"

def get_office_web_address(candidate_id):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Address.getOfficeWebAddress?key={api_key}&candidateId={candidate_id}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error accessing the API: {response.status_code}"

def get_vetoes(candidate_id):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Votes.getVetoes?key={api_key}&candidateId={candidate_id}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error accessing the API: {response.status_code}"

def get_candidates_by_zip(zipcode):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Candidates.getByZip?key={api_key}&zip5={zipcode}&o=JSON"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        candidates = data.get('candidateList', {}).get('candidate', [])
        return candidates
    else:
        return f"Error accessing the API: {response.status_code}"

def get_candidates_by_lastname(lastname):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Candidates.getByLastname?key={api_key}&o=JSON&lastName={lastname}"

    response = requests.get(url)

    if response.status_code == 200:
        candidates = response.json().get('candidateList', {}).get('candidate', [])
        return candidates
    else:
        return f"Error accessing the API: {response.status_code}"

def main():
    st.sidebar.title("Candidate Information Inquiry")

    # Toggle for searching by ZIP code
    use_zipcode = st.sidebar.checkbox("Search by ZIP code")

    if use_zipcode:
        st.sidebar.write("---")
        zipcode = st.sidebar.text_input("Enter ZIP code:")
        if zipcode:
            view_as = st.sidebar.radio("View as:", ["JSON", "Table"])
            candidates_data = get_candidates_by_zip(zipcode)
            if isinstance(candidates_data, str):
                st.error(candidates_data)
            else:
                if view_as == "JSON":
                    st.json(candidates_data)
                else:
                    # Extrair as chaves dos dicionários dos candidatos
                    candidate_keys = list(candidates_data[0].keys()) if candidates_data else []

                    # Permitir que o usuário selecione quais chaves incluir na tabela
                    selected_keys = st.multiselect("Select keys for table:", candidate_keys)

                    if selected_keys:
                        # Filtrar os dados com base nas chaves selecionadas
                        filtered_candidates_data = [{key: candidate[key] for key in selected_keys} for candidate in candidates_data]
                        df = pd.DataFrame(filtered_candidates_data)
                        st.write("### Candidates Found by ZIP Code")
                        st.write(df)
                    else:
                        st.write("Please select keys to display in the table.")
    else:
        # Sidebar menu to select category
        category = st.sidebar.radio("Select category:", ["Biography", "Address", "Votes"])

        search_type = st.sidebar.radio("Select search type:", ["ID", "Last Name"])

        if search_type == "ID":
            candidate_id = st.text_input("Enter candidate ID:")
        else:
            lastname = st.text_input("Enter candidate last name:")
            candidates = get_candidates_by_lastname(lastname)
            if candidates:
                if isinstance(candidates, dict):
                    candidate_id = candidates['candidateId']
                elif len(candidates) == 1:
                    candidate_id = candidates[0]['candidateId']
                else:
                    selected_candidate = st.selectbox("Select candidate:", [candidate['ballotName'] for candidate in candidates])
                    candidate_id = [candidate['candidateId'] for candidate in candidates if candidate['ballotName'] == selected_candidate][0]
            else:
                st.write("No candidates found for the given last name.")
                candidate_id = None

        if candidate_id or search_type == "ID":
            if category == "Biography":
                detailed_bio_option = st.checkbox("Detailed biography")
                bio_data = get_candidate_bio(candidate_id, detailed_bio_option)
                if isinstance(bio_data, str):
                    st.error(bio_data)
                else:
                    if detailed_bio_option:
                        st.write("### Detailed Biography")
                    else:
                        st.write("### Biography")
                    st.json(bio_data)
            elif category == "Address":
                option = st.selectbox("Select address type:", ["Campaign Address", "Campaign Web Address", "Office Address", "Office Web Address"])
                if option == "Campaign Address":
                    address_data = get_campaign_address(candidate_id)
                    if isinstance(address_data, str):
                        st.error(address_data)
                    else:
                        st.write("### Campaign Address")
                        st.json(address_data)
                elif option == "Campaign Web Address":
                    address_data = get_campaign_web_address(candidate_id)
                    if isinstance(address_data, str):
                        st.error(address_data)
                    else:
                        st.write("### Campaign Web Address")
                        st.json(address_data)
                elif option == "Office Address":
                    address_data = get_office_address(candidate_id)
                    if isinstance(address_data, str):
                        st.error(address_data)
                    else:
                        st.write("### Office Address")
                        st.json(address_data)
                else:
                    address_data = get_office_web_address(candidate_id)
                    if isinstance(address_data, str):
                        st.error(address_data)
                    else:
                        st.write("### Office Web Address")
                        st.json(address_data)
            else:
                votes_data = get_vetoes(candidate_id)
                if isinstance(votes_data, str):
                    st.error(votes_data)
                else:
                    st.write("### Vetoes")
                    st.json(votes_data)

if __name__ == "__main__":
    main()
