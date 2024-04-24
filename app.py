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

def get_candidate_id_by_lastname(lastname):
    api_key = "248d31121d86efe50494ae7ee0576fb3"
    url = f"http://api.votesmart.org/Candidates.getByLastname?key={api_key}&o=JSON&lastName={lastname}"

    response = requests.get(url)

    if response.status_code == 200:
        candidates = response.json().get('candidateList', {}).get('candidate', [])
        if candidates:
            # Returns the ID of the first candidate from the list (if any)
            return candidates['candidateId']
        else:
            return None
    else:
        return f"Error accessing the API: {response.status_code}"

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
            st.write("### Candidates Found by ZIP Code")
            if view_as == "JSON":
                st.json(candidates_data)
            else:
                df = pd.DataFrame(candidates_data)
                st.write(df)
else:
    # Sidebar menu to select category
    category = st.sidebar.radio("Select category:", ["Biography", "Address", "Votes"])

    search_type = st.sidebar.radio("Select search type:", ["ID", "Last Name"])

    if search_type == "ID":
        candidate_id = st.text_input("Enter candidate ID:")
    else:
        lastname = st.text_input("Enter candidate last name:")
        candidate_id = get_candidate_id_by_lastname(lastname)

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

